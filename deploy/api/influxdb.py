from django.http import JsonResponse
from authentication.api import base_func
from deploy.tools import ansible2_api
from deploy.api.basic import dict2str


# 安装JDK接口
@base_func.login_check
def install_influxdb(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', 'ERROR')
        port = request.POST.get('port', 'ERROR')
        username = request.POST.get('username', 'ERROR')
        password = request.POST.get('password', 'ERROR')
        influxdb_workpath = request.POST.get('influxdb_workpath', 'ERROR')
        influxdb_port = request.POST.get('influxdb_port', 'ERROR')
        influxdb_password = request.POST.get('influxdb_password', 'ERROR')
        close_selinux = request.POST.get('close_selinux', 'ERROR')
        close_firewall = request.POST.get('close_firewall', 'ERROR')

        if ip == port == username == password == influxdb_workpath == influxdb_port == influxdb_password == close_firewall == close_selinux == "ERROR":
            data = {
                'msg': '从前端获取参数失败',
                'status': 500
            }
            return JsonResponse(data)

        else:
            # 组装数据
            resource = [{
                'hostname': ip,
                'ip': ip,
                'port': port,
                'username': username,
                'password': password,
                'CLOSE_SELINUX': close_selinux,
                'CLOSE_FIREWALL': close_firewall,
                'INFLUXDB_WORKPATH': influxdb_workpath,
                'INFLUXDB_PORT': influxdb_port,
                'INFLUXDB_PASSWORD': influxdb_password
            }]
            try:
                ans = ansible2_api.ANSRunner(resource)
                # 这里传入的是playbook文件和全局参数,playbook文件在项目下，所需的文件都在/cmdb_software下
                ans.run_playbook(playbook_path='deploy/playbook/influxdb.yml', extra_vars=None)
                playbook_result = ans.get_playbook_result()


                # 组装返回给前端的信息
                # 这个状态码
                status = list(playbook_result.get('status').values())[0]
                skipped = dict2str(playbook_result.get('skipped'))
                failed = dict2str(playbook_result.get('failed'))
                ok = dict2str(playbook_result.get('ok'))
                unreachable = dict2str(playbook_result.get('unreachable'))
                # 这个changed好像在ansible api中并没有截取到真实的日志信息，只有返回条数
                changed = dict2str(playbook_result.get('changed'))

                data = {
                    'msg': 'ansible返回信息',
                    'status': 200,
                    'data': {
                        'skipped': skipped,
                        'failed': failed,
                        'ok': ok,
                        'status': status,
                        'unreachable': unreachable,
                        'changed': changed,
                    }
                }

                return JsonResponse(data)
            except Exception as e:
                print(e)
                data = {
                    'msg': 'ansible执行任务失败' + str(e),
                    'status': 500,
                }
                return JsonResponse(data)
