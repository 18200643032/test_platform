from django.db import models
from datetime import datetime
# Create your models here.
class User(models.Model):
    """用户表"""
    gender = (
        ('male','男'),
        ('female','女')
    )
    name = models.CharField(max_length=128,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=256,verbose_name="密码")
    email = models.EmailField(unique=True,verbose_name="邮箱")
    sex = models.CharField(max_length=32,choices=gender,default="男",verbose_name="性别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['add_time']
        verbose_name = "用户"
        verbose_name_plural = "用户"

