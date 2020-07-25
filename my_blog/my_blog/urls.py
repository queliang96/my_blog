"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#记得引入include
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
from article.views import article_list
#存放映射关系的列表
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',article_list,name='home'),
    # 新增代码，配置app的url
    path('article/',include('article.urls',namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),
    path('comment/',include('comment.urls',namespace='comment')),
    #注意这里的notifications.urls没有像之前一样用字符串，是为了确保模块安装到正确的命名空间中。
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls', namespace='notice')),
]
#为以后上传的图片配置好了URL路径。
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)