from django.shortcuts import render,redirect
#导入自带的,登录时的验证函数authentic,用户登录函数login,用户退出函数logout
from django.contrib.auth import authenticate,login,logout
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile


#from userprofile.models import User
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

# Create your views here.
#用户登录验证，如果是用Django自带的auth_user用户，需要用authentic函数验证。
'''def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username)  # 查看数据库里是否有该用户名
            if user:  # 如果存在
                # 将用户数据保存在 session 中，即实现了登录动作

                if user.password == password:
                    return redirect('article:article_list')
                else:
                    context = {'message': "密码错误", 'form': user_login_form}  # 返回表单和提示语，注意千万不腰忘了表单
                    return render(request, 'userprofile/login.html', context)
            else:
                context = {'message':"此用户不存在",'form':user_login_form}
                return render(request,'userprofile/login.html',context)#返回表单和提示语,注意千万不要漏了表单

        else:
            message = "表单内容有误，请重新输入"
            return render(request, 'userprofile/login.html', {'message': message,'form':user_login_form})
    else:
        user_login_form = UserLoginForm()
        return render(request, 'userprofile/login.html',{'form':user_login_form})'''

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .获取表单数据
            username = request.POST.get('username')
            password = request.POST.get('password')
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=username, password=password)
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("article:article_list")
            else:
                context = {'message': "用户名或密码不正确", 'form':user_login_form}
                return render(request, 'userprofile/login.html', context)
        else:
            context = {'message': "输入内容不规范，请重新输入", 'form':user_login_form}
            return render(request, 'userprofile/login.html', context)
    else:
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)

#用户退出
def user_logout(request):
    #Django自带的退出登录函数
    logout(request)
    return redirect('article:article_list')

#用户注册
def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            if password1 != password2:
                context = {'message':"两次输入密码不一致",'user_register':user_register_form}
                return render(request, 'userprofile/register.html', context)
            else:
                user_name = User.objects.filter(username=username)
                if user_name:
                    context = {'message': "用户已存在", 'user_register':user_register_form}
                    return render(request, 'userprofile/register.html', context)
                user_email = User.objects.filter(email=email)
                if user_email:
                    context = {'message': "该邮箱已被注册", 'user_register':user_register_form}
                    return render(request, 'userprofile/register.html', context)
            #自带的user创建普通用户，create_user
            new_user = User.objects.create_user(username=username,password=password1,email=email)
            #注册成功后返回到登录页面
            return redirect('userprofile:login')
        else:
            context = {'message': "输入内容不规范，请重新输入", 'user_register':user_register_form}
            return render(request, 'userprofile/register.html', context)
    else:
        user_register_form = UserRegisterForm()
        context = {'user_register':user_register_form}
        return render(request, 'userprofile/register.html', context)

#删除用户
#@login_required是一个Python装饰器。装饰器可以在不改变某个函数内容的前提下，给这个函数添加一些功能。
#具体来说@login_required要求调用user_delete()函数时，用户必须登录；如果未登录则不执行函数，将页面重定向到/userprofile/login/地址去。

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            #退出登录，删除数据并返回博客列表
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


# 编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    #旧代码
    #profile = Profile.objects.get(user_id=id)
    #去除信号修改后的代码
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

