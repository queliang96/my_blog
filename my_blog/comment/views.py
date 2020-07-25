from django.shortcuts import render,redirect,get_object_or_404
from comment.models import Comment
from comment.forms import CommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from article.models import ArticlePost
from django.contrib.auth.models import User
from notifications.signals import notify
# Create your views here.
#文章评论
@login_required(login_url='/userprofile/login/')
#评论必须关联在某篇具体的文章里，因此需传入文章的id,注意这边article_id只是一个变量而已，可以用任何合法的变量代替，也可以是id
#视图的参数新增了parent_comment_id=None。此参数代表父评论的id值，若为None则表示评论为一级评论，若有具体值则为多级评论。
def post_comment(request,article_id,parent_comment_id=None):
    article = get_object_or_404(ArticlePost,id=article_id) #前面红色的id是Django自动生成的数据表的主键（即pk）
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            #添加二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                #若评论回复超过二级，则转换为2级
                new_comment.parent_id = parent_comment.get_root().id
                #被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 新增消息通知代码，给其他用户发送通知
                if not parent_comment.user.is_superuser and not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient = parent_comment.user,
                        verb = "回复了你",
                        target = article,
                        action_object = new_comment,
                    )
                return HttpResponse('200 OK')
            new_comment.save()
            # 新增消息通知代码，给管理员发送通知
            if not request.user.is_superuser:
                if article.author.is_superuser:
                    notify.send(
                        request.user,
                        recipient = User.objects.filter(is_superuser=1),
                        verb = "回复了你",
                        target = article,
                        action_object = new_comment,
                    )
                else:
                    notify.send(
                        request.user,
                        recipient = article.author,
                        verb = "回复了你",
                        target = article,
                        action_object = new_comment,
                    )
            # 使用视图拼接法添加锚点,使用户发送评论后，能直接回到发表的评论内容处。
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
            # 发送评论后返回当前评论的文章详情页，注意必须同时传入当前文章的id。另外还有一种方法也可返回当前文章详情页，请参考www.dusaiphoto.com/article/detail/49
            #return redirect('article:article_detail',id=article_id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    #处理GET请求,新增处理GET请求的逻辑，用于给二级回复提供空白的表单
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")

 #删除评论
@login_required(login_url='/userprofile/login/')
def comment_delete(request,article_id,comment_id):
    article = ArticlePost.objects.get(id=article_id)
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    #删除评论后回到当前文章详情页，注意必须同时传入当前文章的id。
    return redirect('article:article_detail',id=article_id)
