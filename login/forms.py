from django import forms
from captcha.fields import CaptchaField


class SearchForm(forms.Form):
    search = forms.CharField(label="查询", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))

class UserForm(forms.Form):
    # 表单，方便html部分快速输入
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "请输入不超过8位昵称"}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "请输入8~20位密码"}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "再次输入密码"}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": "请正确输入邮箱"}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
