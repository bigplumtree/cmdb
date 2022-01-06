# 这个是基础功能接口
# 测试主机是否可联通
# 查看主机防火墙和selinux是否开启
# 关闭防火墙
# 关闭selinux

from django.http import JsonResponse
from authentication.api import base_func
from deploy.tools import ansible2_api
from deploy.models import SoftList
# 这个是判断不相等的模块
from django.db.models import Q


# 字典转字符串并加换行的方法
def dict2str(old_dict):
    new_str = ''
    for key, value in old_dict.items():
        new_str += str(key) + ':' + str(value) + '\n'
    return new_str


# 获取软件列表
@base_func.login_check
def get_softlist(request):
    if request.method == 'GET':
        try:
            result = []
            softlist = SoftList.objects.filter(is_del=0)
            for soft in softlist:
                soft_id = soft.id
                soft_name = soft.soft_name
                soft_img = soft.soft_img
                soft_path = soft.soft_path
                soft_desc = soft.soft_desc
                result.append({'soft_id': soft_id,
                               'soft_name': soft_name,
                               'soft_img': soft_img,
                               'soft_path': soft_path,
                               'soft_desc': soft_desc})

            data = {
                'msg': '获取软件列表成功',
                'status': 200,
                'data': result
            }
            return JsonResponse(data)

        except:
            data = {
                'msg': '从数据库中获取软件列表失败',
                'status': 500,
            }
            return JsonResponse(data)


# 检查主机是否可以联通
@base_func.login_check
def host_ping(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', 'ERROR')
        port = request.POST.get('port', 'ERROR')
        username = request.POST.get('username', 'ERROR')
        password = request.POST.get('password', 'ERROR')

        if ip == port == username == password == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 500
            }
            return JsonResponse(data)
        else:
            host_list = [ip]
            resource = [{
                'hostname': ip,
                'ip': ip,
                'port': port,
                'username': username,
                'password': password
            }]
            try:
                ad_hoc = ansible2_api.ANSRunner(resource)
                ad_hoc.run_model(host_list=host_list, module_name='ping', module_args='')
                ad_hoc_result = ad_hoc.get_model_result()

                success = ad_hoc_result.get('success')
                failed = ad_hoc_result.get('failed')
                unreachable = ad_hoc_result.get('unreachable')

                data = {'msg': '字符串拼接失败', 'status': 600, 'data': ad_hoc_result}

                if success:
                    data = {'msg': '主机可以连通', 'status': 200, 'data': success}
                elif failed:
                    data = {'msg': '连接错误', 'status': 590, 'data': failed}
                elif unreachable:
                    data = {'msg': '主机连接失败', 'status': 591, 'data': unreachable}

                return JsonResponse(data)

            except Exception as e:

                data = {
                    'msg': 'ansible工具类调用失败',
                    'status': 599,
                    'data': e
                }
                return JsonResponse(data)
