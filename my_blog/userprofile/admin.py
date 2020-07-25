from django.contrib import admin
from userprofile.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
#admin.site.register(User)
#前面我们已经尝试过将article配置到admin后台，方法是非常简单的，直接在admin.py中写入admin.site.register(Profile)就可以了。
# 但是这样写会导致User、Profile是两个分开的表，不方便不说，强迫症的你怎么能受得了。
#我们希望能够在admin中将User、Profile合并为一张完整的表格。方法如下：

# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)