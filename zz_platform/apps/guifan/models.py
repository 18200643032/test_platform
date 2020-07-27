from django.db import models
from datetime import datetime
# Create your models here.

#容器状态[0是停止。1是运行中]
class GuiFan(models.Model):
    images = models.CharField(max_length=200,verbose_name="镜像名",help_text="镜像名")
    code = models.CharField(max_length=20,verbose_name="容器状态",default=0,help_text="容器状态")
    container_id = models.CharField(max_length=50,verbose_name="容器ID",help_text="容器ID")
    version_opencv = models.CharField(max_length=20,verbose_name="opencv的版本",help_text="opencv的版本")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name ="guifan"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.container_id

