"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from assets.api import menu as assets_menu
from assets.api import engine as assets_engine
from assets.api import project as assets_project
from assets.api import server as assets_server
from assets.api import services as assets_services
from assets.api import collections as assets_collections
from deploy.api import basic as deploy_basic
from deploy.api import jdk as deploy_jdk
from deploy.api import server_init as server_init
from deploy.api import mysql as deploy_mysql
from deploy.api import redis as deploy_redis
from deploy.api import influxdb as deploy_influxdb
from deploy.api import minio as deploy_minio
from deploy.api import nodejs as deploy_nodejs
from deploy.api import mongodb as deploy_mongodb
from authentication.api import base_func


urlpatterns = [
    path('admin/', admin.site.urls),
    # 登陆接口
    re_path('^api/login/$', base_func.login),
    # 获取菜单列表接口
    re_path('^api/assets/menus/$', assets_menu.get_menus),
    # 获取和添加机房接口
    re_path('^api/assets/engineroom/$', assets_engine.engine),
    # 更改机房状态接口
    re_path('^api/assets/engineroom/state/$', assets_engine.engine_state),
    # 编辑机房接口
    re_path('^api/assets/engineroom/edit/$', assets_engine.engine_edit),
    # 删除机房接口
    re_path('^api/assets/engineroom/delete/$', assets_engine.engine_delete),
    # 获取和添加项目接口
    re_path('^api/assets/project/$', assets_project.project),
    # 更改项目状态接口
    re_path('^api/assets/project/state/$', assets_project.project_state),
    # 编辑项目接口
    re_path('^api/assets/project/edit/$', assets_project.project_edit),
    # 删除项目接口
    re_path('^api/assets/project/delete/$', assets_project.project_delete),
    # 获取服务器接口
    re_path('^api/assets/server/$', assets_server.server),
    # 获取服务器echart图表接口
    re_path('^api/assets/server/echart/$', assets_server.server_echart),
    # 编辑服务器接口
    re_path('^api/assets/server/edit/$', assets_server.server_edit),
    # 删除服务器接口
    re_path('^api/assets/server/delete/$', assets_server.server_delete),
    # 获取服务列表接口
    re_path('^api/assets/services/$', assets_services.services),
    # 删除服务列表接口
    re_path('^api/assets/services/delete/$', assets_services.services_delete),
    # 编辑服务列表接口
    re_path('^api/assets/services/edit/$', assets_services.services_edit),
    # 上传服务配置文件接口，查看配置文件列表接口
    re_path('^api/assets/services/configfile/$', assets_services.services_configfile),
    # 删除配置文件接口
    re_path('api/assets/services/configfile/delete/$', assets_services.services_configfile_delete),
    # 获取配置文件内容接口
    re_path('api/assets/services/configfile/txt/$', assets_services.configfile),
    # 获取服务器使用率接口
    re_path('api/assets/serverrate/$', assets_server.server_rate),
    # 获取级联选择框数据接口
    re_path('^api/assets/server/cascader/$', assets_collections.server_cascader),




    ######################################下面是安装部署接口
    # 获取软件列表接口
    re_path('^api/deploy/softlist/$', deploy_basic.get_softlist),
    # 获取机器连接状态接口
    re_path('^api/deploy/machine/state/$', deploy_basic.host_ping),
    # 初始化服务器
    re_path('^api/deploy/server/init/$', server_init.server_init),
    # jdk的安装和卸载
    re_path('^api/deploy/jdk/install/$', deploy_jdk.install_jdk),
    # mysql的安装和卸载
    re_path('^api/deploy/mysql/install/$', deploy_mysql.install_mysql),
    # redis的安装和卸载
    re_path('^api/deploy/redis/install/$', deploy_redis.install_redis),
    # influxdb的安装和卸载
    re_path('^api/deploy/influxdb/install/$', deploy_influxdb.install_influxdb),
    # minio的安装和卸载
    re_path('^api/deploy/minio/install/$', deploy_minio.install_minio),
    # nodejs的安装和卸载
    re_path('^api/deploy/nodejs/install/$', deploy_nodejs.install_nodejs),
    # mongodb的安装和卸载
    re_path('^api/deploy/mongodb/install/$', deploy_mongodb.install_mongodb),
]
