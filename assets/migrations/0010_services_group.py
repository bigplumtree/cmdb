# Generated by Django 3.0.5 on 2021-11-03 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='group',
            field=models.CharField(help_text='启动组', max_length=100, null=True, verbose_name='启动组'),
        ),
    ]
