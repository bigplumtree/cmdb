# Generated by Django 3.0.5 on 2021-10-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20211014_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='项目名称', max_length=30, unique=True, verbose_name='项目名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('text', models.CharField(help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('is_del', models.CharField(default=0, help_text='有效状态', max_length=1, verbose_name='有效状态')),
            ],
            options={
                'verbose_name_plural': '项目',
                'db_table': 'cmdb_project',
            },
        ),
    ]
