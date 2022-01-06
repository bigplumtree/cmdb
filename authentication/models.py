from django.db import models


class CmdbAuth(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False, verbose_name='用户名', help_text='用户名')
    password = models.CharField(max_length=100, null=False, verbose_name='密码', help_text='密码')
    token = models.CharField(max_length=255, null=False, verbose_name='验证字符串', help_text='验证字符串')
    is_admin = models.CharField(max_length=1, default=0, null=False, verbose_name='管理员', help_text='管理员')
    is_del = models.CharField(max_length=1, default=0, null=False, verbose_name='是否有效', help_text='是否有效')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'cmdb_auth'
        verbose_name_plural = '登录认证'