# Generated by Django 3.0.5 on 2021-11-04 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_services_enable_comm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='enable_comm',
            field=models.CharField(default='/', help_text='开机启动命令', max_length=1000, null=True, verbose_name='开机启动命令'),
        ),
        migrations.AlterField(
            model_name='services',
            name='group',
            field=models.CharField(default='/', help_text='启动组', max_length=100, null=True, verbose_name='启动组'),
        ),
        migrations.AlterField(
            model_name='services',
            name='owner',
            field=models.CharField(default='/', help_text='启动用户', max_length=100, null=True, verbose_name='启动用户'),
        ),
        migrations.AlterField(
            model_name='services',
            name='password',
            field=models.CharField(default='/', help_text='密码', max_length=100, null=True, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='services',
            name='restart_comm',
            field=models.CharField(default='/', help_text='重启命令', max_length=1000, null=True, verbose_name='重启命令'),
        ),
        migrations.AlterField(
            model_name='services',
            name='service_dir',
            field=models.CharField(default='/', help_text='安装目录', max_length=1000, null=True, verbose_name='安装目录'),
        ),
        migrations.AlterField(
            model_name='services',
            name='service_port',
            field=models.CharField(default='/', help_text='服务端口', max_length=100, null=True, verbose_name='服务端口'),
        ),
        migrations.AlterField(
            model_name='services',
            name='service_version',
            field=models.CharField(default='/', help_text='服务版本', max_length=100, null=True, verbose_name='服务版本'),
        ),
        migrations.AlterField(
            model_name='services',
            name='start_comm',
            field=models.CharField(default='/', help_text='启动命令', max_length=1000, null=True, verbose_name='启动命令'),
        ),
        migrations.AlterField(
            model_name='services',
            name='stop_comm',
            field=models.CharField(default='/', help_text='停止命令', max_length=1000, null=True, verbose_name='停止命令'),
        ),
        migrations.AlterField(
            model_name='services',
            name='username',
            field=models.CharField(default='/', help_text='用户名', max_length=100, null=True, verbose_name='用户名'),
        ),
    ]
