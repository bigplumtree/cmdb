from django.http import JsonResponse
from assets.models import Services, ServiceConfig
# 这个是判断不相等的模块
from django.db.models import Q
from authentication.api import base_func
import io
import random
import string
from minio import Minio
from minio.error import InvalidResponseError


# 获取服务器列表
@base_func.login_check
def services(request):
    if request.method == 'GET':
        server_id = request.GET.get('server_id', 'ERROR')

        if server_id == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 501,
            }
            return JsonResponse(data)
        else:
            try:
                services_list = []
                all_services = Services.objects.filter(belong_server__id=server_id)
                for s in all_services:
                    service_id = s.id
                    service_name = s.service_name
                    service_port = s.service_port
                    service_dir = s.service_dir
                    service_version = s.service_version
                    service_owner = s.owner
                    service_group = s.group
                    service_username = s.username
                    service_password = s.password
                    service_start_comm = s.start_comm
                    service_stop_comm = s.stop_comm
                    service_restart_comm = s.restart_comm
                    service_enable_comm = s.enable_comm
                    service_text = s.text
                    services_list.append({
                        'service_id': service_id,
                        'service_name': service_name,
                        'service_port': service_port,
                        'service_dir': service_dir,
                        'service_version': service_version,
                        'service_owner': service_owner,
                        'service_group': service_group,
                        'service_username': service_username,
                        'service_password': service_password,
                        'service_start_comm': service_start_comm,
                        'service_stop_comm': service_stop_comm,
                        'service_restart_comm': service_restart_comm,
                        'service_enable_comm': service_enable_comm,
                        'service_text': service_text})

                data = {
                    'msg': '获取成功',
                    'status': 200,
                    'data': services_list
                }
                return JsonResponse(data)
            except:

                data = {
                    'msg': '从数据库中获取失败',
                    'status': 500,
                }
                return JsonResponse(data)

    if request.method == 'POST':
        server_id = request.POST.get('server_id', 'ERROR')
        name = request.POST.get('name', 'ERROR')
        path = request.POST.get('path', '/')
        port = request.POST.get('port', '/')
        username = request.POST.get('username', '/')
        password = request.POST.get('password', '/')
        version = request.POST.get('version', '/')
        owner = request.POST.get('owner', '/')
        group = request.POST.get('group', '/')
        startcmd = request.POST.get('startcmd', '/')
        restartcmd = request.POST.get('restartcmd', '/')
        stopcmd = request.POST.get('stopcmd', '/')
        enablecmd = request.POST.get('enablecmd', '/')
        text = request.POST.get('text')

        if server_id == name == 'ERROR':
            data = {
                'status': 501,
                'msg': '从前端获取参数失败'
            }
            return JsonResponse(data)
        else:
            try:
                Services.objects.create(belong_server_id=server_id,
                                        service_name=name,
                                        service_dir=path,
                                        service_port=port,
                                        username=username,
                                        password=password,
                                        service_version=version,
                                        owner=owner,
                                        group=group,
                                        start_comm=startcmd,
                                        restart_comm=restartcmd,
                                        stop_comm=stopcmd,
                                        enable_comm=enablecmd,
                                        text=text)
                data = {
                    'status': 200,
                    'msg': '添加成功'
                }
                return JsonResponse(data)
            except:
                data = {
                    'status': 500,
                    'msg': '在数据库中添加失败'
                }
                return JsonResponse(data)


# 删除服务器列表
@base_func.login_check
def services_delete(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id', 'ERROR')
        if service_id == 'ERROR':
            data = {
                'status': 501,
                'msg': '从前端获取参数失败'
            }
            return JsonResponse(data)
        else:
            try:
                Services.objects.filter(id=service_id).delete()
                data = {
                    'status': 200,
                    'msg': '删除成功'
                }
                return JsonResponse(data)
            except Exception as e:
                print(e)
                data = {
                    'status': 500,
                    'msg': '在数据库中删除失败'
                }
                return JsonResponse(data)


# 编辑服务接口
@base_func.login_check
def services_edit(request):
    service_id = request.POST.get('service_id', 'ERROR')
    name = request.POST.get('name', 'ERROR')
    path = request.POST.get('path', '/')
    port = request.POST.get('port', '/')
    username = request.POST.get('username', '/')
    password = request.POST.get('password', '/')
    version = request.POST.get('version', '/')
    owner = request.POST.get('owner', '/')
    group = request.POST.get('group', '/')
    startcmd = request.POST.get('startcmd', '/')
    restartcmd = request.POST.get('restartcmd', '/')
    stopcmd = request.POST.get('stopcmd', '/')
    enablecmd = request.POST.get('enablecmd', '/')
    text = request.POST.get('text')

    if service_id == name == 'ERROR':
        data = {
            'status': 501,
            'msg': '从前端获取参数失败'
        }
        return JsonResponse(data)
    try:
        s = Services.objects.get(id=service_id)
        s.service_name = name
        s.service_port = port
        s.service_dir = path
        s.service_version = version
        s.owner = owner
        s.group = group
        s.username = username
        s.password = password
        s.start_comm = startcmd
        s.restart_comm = restartcmd
        s.stop_comm = stopcmd
        s.enable_comm = enablecmd
        s.text = text
        s.save()
        data = {
            'status': 200,
            'msg': '更新成功'
        }
        return JsonResponse(data)
    except:
        data = {
            'status': 500,
            'msg': '在数据库中更新失败'
        }
        return JsonResponse(data)


# 上传服务配置文件/获取服务对应配置文件列表接口(弹出框弹出时，展示的配置文件列表)
@base_func.login_check
def services_configfile(request):
    if request.method == 'GET':
        service_id = request.GET.get('service_id', 'ERROR')
        if service_id == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 501
            }
            return JsonResponse(data)
        else:

            try:
                service_configfile_list = []

                configfiles = ServiceConfig.objects.filter(belong_service_id=service_id)

                if len(configfiles) == 0:
                    data = {
                        'status': 200,
                        'msg': '获取配置文件成功',
                        'data': service_configfile_list
                    }
                    return JsonResponse(data)
                else:
                    for cf in configfiles:
                        config_name = cf.config_name
                        config_hash = cf.config_hash
                        config_size = cf.file_size
                        config_type = cf.file_type
                        config_id = cf.id
                        service_configfile_list.append({
                            'name': config_name,
                            'hash': config_hash,
                            'size': config_size,
                            'type': config_type,
                            'id': config_id
                        })

                    data = {
                        'status': 200,
                        'msg': '获取配置文件成功',
                        'data': service_configfile_list
                    }
                    return JsonResponse(data)
            except:
                data = {
                    'status': 500,
                    'msg': '在数据库中获取配置文件信息失败',
                }
                return JsonResponse(data)
    if request.method == 'POST':
        service_id = request.POST.get('service_id', 'ERROR')
        if request.FILES and service_id != 'ERROR':
            # 这个serviceConfigFile是前端的上传框的name值
            service_config_file = request.FILES.get('serviceConfigFile')

            if service_config_file:
                # 前端会过滤一次文件大小，但是这里做的完善一些在判断一次文件大小
                file_size = int(service_config_file.size)
                if file_size/1024/1024 > 50:
                    data = {
                        'status': 510,
                        'msg': '上传文件不能大于50M'
                    }
                    return JsonResponse(data)
                else:
                    try:
                        # 将前端传过来的文件转换成流，这样就可以使用minio的流上传方式进行上传
                        file_io = io.BytesIO(service_config_file.read())
                        file_size = service_config_file.size
                        file_type = service_config_file.content_type
                        file_charset = service_config_file.charset
                        # 原始文件名存放在mysql数据库中，需要和hash字符串一一对应上
                        file_name_meta = service_config_file.name
                        # minio存储时，需要存储这50个随机字符串，不然可能文件名会冲突
                        file_name_hash = ''.join(random.sample(string.digits + string.ascii_letters, 50))

                        from cmdb.settings import MINIO_URL, MINIO_SSL, MINIO_USERNAME, MINIO_PASSWORD, MINIO_CONFIGFILE_BUCKET

                        # 初始化minio
                        minio_client = Minio(endpoint=MINIO_URL,
                                             access_key=MINIO_USERNAME,
                                             secret_key=MINIO_PASSWORD,
                                             secure=MINIO_SSL)

                        # 判断存储通是否存在，不存在就创建
                        if not minio_client.bucket_exists(MINIO_CONFIGFILE_BUCKET):
                            minio_client.make_bucket(MINIO_CONFIGFILE_BUCKET, location='cn-north-1')

                        # 上传文件
                        minio_client.put_object(bucket_name=MINIO_CONFIGFILE_BUCKET,
                                                object_name=file_name_hash,
                                                data=file_io,
                                                length=file_size,
                                                content_type=file_type
                                                )

                        # 上传成功后在mysql中建立文件对应关系
                        ServiceConfig.objects.create(belong_service_id=service_id,
                                                     config_name=file_name_meta,
                                                     config_hash=file_name_hash,
                                                     file_size=file_size,
                                                     file_type=file_type,
                                                     file_charset=file_charset)

                        data = {
                            'status': 200,
                            'msg': '文件上传成功'
                        }
                        return JsonResponse(data)

                    except Exception as e:
                        print(e)
                        data = {
                            'status': 511,
                            'msg': '文件上传失败'
                        }
                        return JsonResponse(data)
        else:
            data = {
                'status': 510,
                'msg': '从前端获取文件或服务ID失败'
            }
            return JsonResponse(data)


# 获取服务配置文件内容接口
@base_func.login_check
def configfile(request):
    if request.method == 'GET':
        config_hash = request.GET.get('config_hash', 'ERROR')
        if config_hash == 'ERROR':
            data = {
                'status': 200,
                'msg': '从前端获取配置文件hash失败',
                'data': '从前端获取配置文件hash失败'
            }
            return JsonResponse(data)
        else:
            try:
                from cmdb.settings import MINIO_URL, MINIO_SSL, MINIO_USERNAME, MINIO_PASSWORD, MINIO_CONFIGFILE_BUCKET

                # 初始化minio
                minio_client = Minio(endpoint=MINIO_URL,
                                     access_key=MINIO_USERNAME,
                                     secret_key=MINIO_PASSWORD,
                                     secure=MINIO_SSL)

                # 获取配置文件内容
                file = minio_client.get_object(bucket_name=MINIO_CONFIGFILE_BUCKET, object_name=config_hash)
                # TODO
                # 这块直接读，如果文件过大内存会溢出，不过在上传的时候已经做了限制应该不会有问题，需要优化
                config_txt = file.read().decode()
                data = {
                    'status': 200,
                    'msg': '获取成功',
                    'data': config_txt
                }
                return JsonResponse(data)
            except:
                data = {
                    'status': 200,
                    'msg': '在MINIO中获取配置文件失败',
                    'data': '在MINIO中获取配置文件失败'
                }
                return JsonResponse(data)


# 服务配置文件删除接口
@base_func.login_check
def services_configfile_delete(request):
    if request.method == 'POST':
        configfile_id = request.POST.get('configfile_id', 'ERROR')
        configfile_hash = request.POST.get('configfile_hash', 'ERROR')
        if configfile_id == configfile_hash == 'ERROR':
            data = {
                'status': 510,
                'msg': '从前端获取配置文件ID失败'
            }
            return JsonResponse(data)
        else:
            try:
                from cmdb.settings import MINIO_URL, MINIO_SSL, MINIO_USERNAME, MINIO_PASSWORD, MINIO_CONFIGFILE_BUCKET

                # 初始化minio
                minio_client = Minio(endpoint=MINIO_URL,
                                     access_key=MINIO_USERNAME,
                                     secret_key=MINIO_PASSWORD,
                                     secure=MINIO_SSL)

                # 在MINIO中删除文件
                minio_client.remove_object(bucket_name=MINIO_CONFIGFILE_BUCKET,
                                           object_name=configfile_hash)

                # 在mysql中删除对应关系
                ServiceConfig.objects.filter(id=configfile_id).delete()
                data = {
                    'status': 200,
                    'msg': '删除成功'
                }
                return JsonResponse(data)
            except:
                data = {
                    'status': 513,
                    'msg': '删除失败'
                }
                return JsonResponse(data)
