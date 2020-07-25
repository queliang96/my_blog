from django.db import models

# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver

# Create your models here.
'''class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(default="")
    def __str__(self):
        # return self.title 将文章标题返回在Django管理后台中做为对象的显示值
        return self.username'''

from django.contrib.auth.models import User


#扩展user用户模型

# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    #upload_to指定了图片上传的位置，即/media/avatar/%Y%m%d/。%Y%m%d是日期格式化的写法，会最终格式化为系统时间。比如说图片
    #上传是2018年12月5日，则图片会保存在/media/avatar/2018205/中。注意ImageField字段不会存储图片本身，而仅仅保存图片的地址。记得用pip指令安装Pillow。
    avatar = models.ImageField(upload_to='profile/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 信号接收函数，每当新建 User 实例时自动调用
'''@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''
