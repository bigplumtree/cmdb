# Generated by Django 3.0 on 2021-12-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0015_serverrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverrate',
            name='update_time',
            field=models.DateTimeField(auto_now=True, help_text='上次更新时间', null=True, verbose_name='上次更新时间'),
        ),
    ]
