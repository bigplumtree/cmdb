from django.db import models


class SoftList(models.Model):
    id = models.AutoField(primary_key=True)
    soft_name = models.CharField(unique=True, max_length=30, null=False, verbose_name='软件名称', help_text='软件名称')
    soft_img = models.TextField(null=True, verbose_name='软件图片', help_text='软件图片base64')
    soft_path = models.CharField(max_length=100, null=False, verbose_name='软件路径', help_text='软件路径，路由跳转路径')
    soft_desc = models.CharField(max_length=255, null=True, verbose_name='软件描述', help_text='软件描述')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_deploy_softlist'
        verbose_name_plural = '软件列表'