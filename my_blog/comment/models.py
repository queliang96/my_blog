from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
# django-ckeditor
from ckeditor.fields import RichTextField
# django-mptt
from mptt.models import MPTTModel,TreeForeignKey
# Create your models here.
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    #body = models.TextField()
    body = RichTextField()
    #auto_now_add为添加时的时间，更新对象时不会有变动；而auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    created = models.DateTimeField(auto_now_add=True)
    #内部类是可选的，定义model的元数据，这些信息不是某篇文章私有的数据，而是整张表的共同行为。

    #新增mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    #新增记录二级评论
    reply_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replyers'
    )
    #class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列.'created'为正序
        #保证了最新的文章总是在网页的最上方。注意ordering是元组，括号中只含一个元素时不要忘记末尾的逗号。
        #ordering = ('created',)

    class MPTTMeta:
        order_insertion_by = ['created']
    def __str__(self):
        return self.body[:20]