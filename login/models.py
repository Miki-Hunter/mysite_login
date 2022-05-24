from django.db import models
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '*')
    )
    name = models.CharField(verbose_name='账号', max_length=128, unique=True)  # 网上昵称，有唯一性
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    sex = models.CharField(verbose_name='性别', max_length=10, choices=gender, default='男')
    c_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    l_score = models.BigIntegerField(verbose_name='积分', default=0)
    l_score_time = models.DateTimeField(verbose_name='最新更新时间', auto_now=True)
    introduce = models.TextField(verbose_name='个人简介', default="这个人太懒了，什么都没有留下")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

# # 名次表
# class Rank(models.Model):
#     c_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,)
#     rank = models.IntegerField(verbose_name='名次', validators=[MinValueValidator(1)])
