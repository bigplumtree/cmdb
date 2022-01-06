"""


django orm添加注释插件（orm在创建表的时候不自动把字段注释加上去需要安装插件）

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(oh8lqx1f$$+d7x*ax+*pcmm&e=%^4$a)q=5=&a&ahif9g8740'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_comment_migrate',
    'corsheaders',
    'assets',
    'authentication',
    'deploy'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
CORS_ALLOW_ALL_ORIGINS =True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'cmdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cmdb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

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


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'



MINIO_URL = 'MINIO_IP'
MINIO_SSL = False
# 配置文件存储桶名称
MINIO_CONFIGFILE_BUCKET = 'MINIO_BUCKET'
MINIO_USERNAME = 'MINIO_USER'
MINIO_PASSWORD = 'MINIO_PASS'


# 查询服务器CPU内存磁盘命令
# 1 5 15分钟的负载
CPU_UTILIZATION_RATE = 'top -bn1 | grep load | awk \'{printf \"%.2f,%.2f,%.2f\", $(NF-2),$(NF-1),$(NF-0)}\''
# 总内存和可用内存
MEM_UTILIZATION_RATE = 'free -m | awk \'NR==2{printf \"%s,%s,%2.2f\",$2,$7,($7/$2*100)}\''
# 挂载路径，总容量，可用容量，已用比例
DISK_UTILIZATION_RATE = 'df -m -t ext2 -t ext3 -t ext4 -t xfs | grep -vE \'^Filesystem|文件系统|tmpfs|cdrom\'  | awk \'{ printf \"%s,%.2f,%.2f,%s;\",$6,($2/1024),($4/1024),$5 }\''
