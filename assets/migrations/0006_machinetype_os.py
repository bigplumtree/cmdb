# Generated by Django 3.0.5 on 2021-10-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20211025_0754'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', help_text='机器类型：虚拟机或物理机', max_length=255, verbose_name='机器类型')),
                ('is_del', models.CharField(default=0, help_text='有效状态', max_length=1, verbose_name='有效状态')),
            ],
            options={
                'verbose_name_plural': '机器类型',
                'db_table': 'cmdb_machine_type',
            },
        ),
        migrations.CreateModel(
            name='Os',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', help_text='操作系统', max_length=255, verbose_name='操作系统')),
                ('is_del', models.CharField(default=0, help_text='有效状态', max_length=1, verbose_name='有效状态')),
            ],
            options={
                'verbose_name_plural': '操作系统',
                'db_table': 'cmdb_os',
            },
        ),
    ]
