from django import forms
from .models import Profile
#引入User模型
from django.contrib.auth.models import User
#用户登录表单,登录的时候提交表单的内容对数据库不产生改变，应该继承forms.Form
#froms.Form它适用于不与数据库进行直接交互的功能。
class UserLoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserRegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="登录密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))

#用户注册表单,注册时表单的内容会保存至数据库，应该继承forms.Modelorm,它适用于需要直接与数据库交互的功能，比如新建、更新数据库的字段等
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')