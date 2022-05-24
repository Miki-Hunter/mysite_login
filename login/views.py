from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm, SearchForm
import hashlib

def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        # 已经登录，跳转主页
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        print(login_form)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            # 取出输入的信息
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print(username, password)
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password) or user.password==password:  # 哈希值和数据库内的值进行比对
                    # 写入状态与数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_score'] = user.l_score
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。可以修改
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = ""
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if len(username)>9:
                message = "您的昵称太长！"
            elif len(password1)<8 or len(password1)>20:
                message = "请输入8~20位密码哦！"
            elif password1 != password2:
                message = "两次输入的密码不同！"
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    same_email_user = models.User.objects.filter(email=email)
                    if same_email_user:  # 邮箱地址唯一
                        message = '该邮箱地址已被注册，请使用别的邮箱！'
                else:
                    new_user = models.User.objects.create()
                    new_user.name = username
                    new_user.password = hash_code(password1)  # 使用加密密码
                    new_user.email = email
                    new_user.sex = sex
                    new_user.save()
                    # 存入数据库  # 当一切都OK的情况下，创建新用户
                    return redirect('/login/')  # 自动跳转到登录页面
        if message:
            return render(request, 'login/register.html',locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush() # 删除当前的会话数据和会话cookie。经常用在用户退出后，删除会话
    # 登出就清除状态 或者使用下面的方法一个一个删,(也许我会留一些想要的。。。)
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    # return redirect("/index/")
    message = "已成功退出登录！"
    return render(request, 'login/index.html', locals())

def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
#
def show(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            username = search_form.cleaned_data['search']
            try:
                user = models.User.objects.get(name=username)
                request.session['is_found'] = True
                request.session['the_score'] = user.l_score
                request.session['the_name'] = user.name
                return render(request, 'login/show.html', locals())
            except:
                message = "用户不存在！"
                request.session['is_found'] = False
    return render(request, 'login/show.html', locals())
def search(request):
    search_form = SearchForm()
    return render(request, 'login/search.html',locals())

def master(request):
    pass
    master_list = models.User.objects.order_by('-l_score')[:5]
    return render(request, 'login/master.html', locals())

