from django.shortcuts import render,redirect
from article.models import ArticlePost,ArticleColumn
from comment.models import Comment
# 引入markdown模块
import markdown
from .forms import ArticlePostForm #引入表单
from django.contrib.auth.models import User # 引入User模型
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#引入分页模块
from django.core.paginator import Paginator
#引入Q对象，可同时查询多个参数
from django.db.models import Q
# 引入评论表单
from comment.forms import CommentForm
# Create your views here.
#文章列表
def article_list(request):
    # 从 url 中提取查询参数，
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column') #list.html中href="{% url 'article:article_list' %}?column={{ article.column.id }}"
    tag = request.GET.get('tag')
    # 初始化查询集
    article_list = ArticlePost.objects.all()
    #搜索查询集
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索, 但是发现一个问题：增加作者后搜索报错Q(author__icontains=search)
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        search = ''
    # 栏目查询集
    if column is not None and column.isdigit():     #str.isdigit()函数检测字符串，若只包含数字则返回 True 否则返回 False
    #if column and column != None:
        article_list = article_list.filter(column=column)
    #标签查询集
    if tag and tag != None:
        #注意Django-taggit中标签过滤的写法：filter(tags__name__in=[tag])，tags字段中过滤name为tag的数据条目。赋值的字符串tag用方括号包起来。
        article_list = article_list.filter(tags__name__in=[tag])

    #查询集排序
    #返回不同排序的对象数组，视图根据GET参数order的值，判断取出的文章如何排序，
    if order == 'total_views':  #这里的order是从模板传递过来的
        article_list = ArticlePost.objects.all().order_by('-total_views')
    #每页显示3篇文章
    paginator = Paginator(article_list,3)
    #获取url中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    #把order也传到模板,因为文章需要翻页！order给模板一个标识，提醒模板下一页应该如何排序,还有search,column,tag
    context = {'articles':articles,'order':order,'search':search,'column':column,'tag':tag,}
    return render(request,'article/list.html',context)

#文章详情页
def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    #新增评论功能，取出文章评论
    comments = Comment.objects.filter(article=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
        ])
    #浏览量+1,只要跳到文章详情页的url,浏览量就加1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 引入评论表单,使富文本编辑器在前台展示
    comment_form = CommentForm()
    return render(request,'article/detail.html',{'article':article,'comments':comments,'comment_form':comment_form})

#创建新的文章
@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":    #判断用户是否提交数据
        article_post_form = ArticlePostForm(request.POST,request.FILES)   # 将提交的数据赋值到表单实例中
        if article_post_form.is_valid():    # 判断提交的数据是否满足模型的要求
            article = article_post_form.save(commit=False)
            article.author = User.objects.get(id=request.user.id)     #author是指向User数据表的外键，author的值为当前登录的用户
            # 新增的代码,这块如果不选择文章栏目，始终会报表单内容错误，说明下面代码未生效。
            if request.POST['column'] != 'none':
                #column是指向ArticleColumn的外键，这边赋值需要与上面的author一样
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            #保存到数据库
            article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            #article.tags.add(request.POST.get('tags')) #model.tags.add()添加标签并保存到数据库，model.tags.all()查询所以标签

            return redirect('article:article_list') #写入新的文章成功返回到文章列表
        else:
            context = {'message': "输入内容不规范，请重新输入", 'article_post_form':article_post_form}
            return render(request, 'article/create.html', context)
    #如果用户是get请求数据，则返回一个空的表单类对象，提供给用户填写。
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        return render(request,'article/create.html',{'article_post_form':article_post_form,'columns':columns})

#删除文章
#非安全方式删除文章
# 检查登录
'''@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('article:article_list')'''

#安全方式删除文章，CSRF令牌
#点击删除文章链接时，弹出 layer 弹窗
#弹窗不再发起 GET 请求，而是通过 Jquery 选择器找到隐藏的表单，并点击发送按钮
#表单发起 POST 请求，并携带了 csrf 令牌，从而避免了 csrf 攻击
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        # 新增过滤非作者的用户
        if request.user != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

#修改文章
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_update(request,id): #这里的id为一个变量，可以用任何合法的变量名代替
    article = ArticlePost.objects.get(id=id)    #获取需要修改的文章对象，前面红色的id为数据表的主键（即pk）,是Django自动生成的，ArticlePost里如果author字段是指向user的外键，自动生成的主键会变为author_id
    # 新增过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            article.title = request.POST.get('title')     #title = request.POST['title'],如果title不存在，提出异常；title = request.POST.get('title')，如果title不存在，返回NOone
            article.body = request.POST.get('body')
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST.get('column'))
            else:
                article.column = None
            #更新标签Model.tags.set(*"newTag", clear=True),clear=True：先会清空旧标签，然后添加新标签，因为tags不是
            #article.tags.set(*request.POST.get('tags').split(','),clear=True)#split()将字符串以逗号为分隔符进行分割后返回一个列表
            article.tags.clear()
            for tag in request.POST['tags'].split(','):
                if tag.strip():
                    article.tags.add(tag)
            #更新标题图
            # 如果 request.FILES 存在文件，则保存。若不加此判断，程序会报错
            if request.FILES.get('avatar'):
                article.avatar = request.FILES['avatar']
            article.save()
            #完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail",id=id)
        else:
            context = {'message': "输入内容不规范，请重新输入", 'article_post_form':article_post_form}
            return render(request, 'article/create.html', context)
    #如果用户是get请求数据，则返回一个空的表单类对象，提供给用户填写。
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        #[x for x in args]遍历args并返回其每个元素使之组成一个列表,
        #articles.tags.names()取出tags的值，返回的是一个列表
        tags = ','.join([x for x in article.tags.names()]) #','.join(seq)以逗号为分隔符，将seq所有的元素合并成一个新的字符串
        context = {'article': article, 'article_post_form': article_post_form,'columns':columns,'tags':tags} #注意要把article传到表单中
        return render(request,'article/update.html',context)