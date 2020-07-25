from django.contrib import admin
# 别忘了导入ArticlerPost
from article.models import ArticlePost,ArticleColumn
# Register your models here.
#admin.site.register(ArticlePost)

#若对后台界面不满意，可以导入ModelAdmin这个类来进行修饰
class Article_post_Admin(admin.ModelAdmin):
    list_display = ['title','author']
admin.site.register(ArticlePost,Article_post_Admin)
#注册文章栏目
admin.site.register(ArticleColumn)
