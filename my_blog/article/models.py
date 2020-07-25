from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
# 导入标签Django-taggit
from taggit.managers import TaggableManager
from django.urls import reverse
from PIL import Image #处理标题图

# Create your models here.
#文章栏目模型,注意ArticleColumn模型必须放在ArticlePost之前，否则后面column=models.ForeignKey....为提示找不到ArticleColumn
class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

#文章模型
class ArticlePost(models.Model):
    # 一个作者对应多篇文章,是一对多的关系。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    body = models.TextField()
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    #文章浏览量
    total_views = models.PositiveIntegerField(default=0)
    #一个栏目对应多篇文章，一篇文章只能对应一个栏目。所以是一对多ForeignKey
    column = models.ForeignKey(ArticleColumn,null=True,blank=True,on_delete=models.CASCADE,related_name='aticle')
    #标签引用的不是内置字段，而是库中的TaggableManager，它是处理多对多关系的管理器
    tags = TaggableManager(blank=True) #一篇文章可以有多个标签，一个标签也可对应多篇文章。所以是多对多的关系。如果不用现成的轮子，需设定ManyToManyField多对多的外键
    #文章标题图
    avatar = models.ImageField(blank=True,upload_to='article/%Y%m%d')
    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        #保证了最新的文章总是在网页的最上方。注意ordering是元组，括号中只含一个元素时不要忘记末尾的逗号。
        ordering = ('-created',)
        verbose_name = '文章'  # 指定后台显示模型名称
        verbose_name_plural = '文章列表'  # 指定后台显示模型复数名称
        db_table = 'article'  # 重新定义数据库名，若不指定，默认为项目app名称+'_'+'小写的数据库class 类名'，例如article_aticlepost

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回在Django管理后台中做为对象的显示值
        return self.title
    # 保存时处理图片,如果不处理。则按默认显示
    '''def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article'''