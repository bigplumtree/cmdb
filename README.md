 **开发环境**

项目需要在Linux环境下进行开发,因为用到了ansible模块,目前没有找到Windows上安装ansible模块的方法
我一直是用一台电脑安装Ubuntu的环境进行开发,Ubuntu下也有pycharm工具

 
 **项目上线** 

操作系统:
- Centos
- Ubuntu

运行环境:
- python-3.6
- Django-3.0

基础组件:
- mysql-5.7
- minio-2020-07-02

1. 先使用pip安装项目所需的三方模块
```
pip install -r requirements.txt
```
2. 使用pip安装uwsgi
```
pip3 install uwsgi -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

3. 在服务器上安装ansible所需的密码登陆模块
- Centos
```
sudo yum install sshpass
```
- Ubuntu
```
sudo apt-get install sshpass
```

4. 拉取项目,更改cmdb/settings.py文件中数据库和minio的连接信息
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MYSQL_DATABASE',   #注意这里的数据库应该以utf-8编码
        'USER': 'MYSQL_USERNAME',
        'PASSWORD': 'MYSQL_PASSWORD',
        'HOST': 'MYSQL_IP',
        'PORT': 'MYSQL_PORT',
        }
}

MINIO_URL = 'MINIO_IP'
MINIO_SSL = False
# 配置文件存储桶名称
MINIO_CONFIGFILE_BUCKET = 'MINIO_BUCKET'
MINIO_USERNAME = 'MINIO_USER'
MINIO_PASSWORD = 'MINIO_PASS'

```
5. 将更改后的文件上传到服务器,以/data/目录为例
```
[root@localhost cmdb]# ll /data/cmdb/
总用量 168
drwxr-xr-x 5 cmdb cmdb   168 12月  8 13:53 assets
drwxr-xr-x 5 cmdb cmdb   153 12月  8 13:53 authentication
drwxr-xr-x 3 cmdb cmdb   108 12月  8 14:25 cmdb
drwxr-xr-x 2 cmdb cmdb    23 12月  8 13:53 conf
drwxr-xr-x 6 cmdb cmdb   166 12月  8 13:53 deploy
-rw-r--r-- 1 cmdb cmdb   624 12月  8 13:53 manage.py
-rw-r--r-- 1 cmdb cmdb  1102 12月  8 13:53 readme.md
-rw-r--r-- 1 cmdb cmdb   372 12月  8 13:53 requirements.txt
-rw-r--r-- 1 cmdb cmdb   712 12月  8 14:24 uwsgi.ini
-rw-r----- 1 cmdb cmdb 84430 12月  8 14:57 uwsgi.log
-rw-r--r-- 1 cmdb cmdb     6 12月  8 14:26 uwsgi.pid
```

6. 启动测试
```
uwsgi --ini uwsgi.ini
```

7. 使用systemd托管
```
[Unit]
Description=cmdb
Documentation=http://www.xxx.com
After=network.target
 
[Service]
User=cmdb
Group=cmdb
WorkingDirectory=/data/cmdb/
ExecStart=/usr/local/bin/uwsgi --ini /data/cmdb/uwsgi.ini
ExecReload=/usr/local/bin/uwsgi --reload /data/cmdb/uwsgi.pid
ExecStop=/usr/local/bin/uwsgi --stop /data/cmdb/uwsgi.pid
Restart=on-failure
RestartSec=20s
 
[Install]
WantedBy=multi-user.target
```

8.安装部署功能，需要在服务器根目录下创建cmdb_software,并将程序包解压到该目录下

程序包下载地址: https://www.aliyundrive.com/s/HAc3QFswohy
```
mkdir /cmdb_software
```
