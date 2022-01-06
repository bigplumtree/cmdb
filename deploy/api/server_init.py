from django.http import JsonResponse
from authentication.api import base_func
from deploy.tools import ansible2_api
from deploy.api.basic import dict2str


# 初始化服务器接口
@base_func.login_check
def server_init(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', 'ERROR')
        port = request.POST.get('port', 'ERROR')
        username = request.POST.get('username', 'ERROR')
        password = request.POST.get('password', 'ERROR')
        close_selinux = request.POST.get('close_selinux', 'ERROR')
        close_firewall = request.POST.get('close_firewall', 'ERROR')
        change_zone = request.POST.get('change_zone', 'ERROR')
        system_tuning = request.POST.get('system_tuning', 'ERROR')
        none_network = request.POST.get('none_network', 'ERROR')
        install_dependencies = request.POST.get('install_dependencies', 'ERROR')
        ntp_server = request.POST.get('ntp_server', 'ERROR')
        work_dir = request.POST.get('work_dir', 'ERROR')

        if ip == port == username == password == work_dir == change_zone == ntp_server == none_network == install_dependencies == system_tuning == close_firewall == close_selinux == "ERROR":
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
                'CHANGE_ZONE': change_zone,
                'SYSTEM_TUNING': system_tuning,
                'NONE_NETWORK': none_network,
                'INSTALL_DEPENDENCIES': install_dependencies,
                'NTP_SERVER': ntp_server,
                'WORK_DIR': work_dir
            }]
            try:
                ans = ansible2_api.ANSRunner(resource)
                # 这里传入的是playbook文件和全局参数,playbook文件在项目下，所需的文件都在/cmdb_software下
                ans.run_playbook(playbook_path='deploy/playbook/server_init.yml', extra_vars=None)
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