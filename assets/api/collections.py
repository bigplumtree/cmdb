# 菜单类
from django.http import JsonResponse
from assets.models import EngineRoom, Project, Os, MachineType, Server
# 这个是判断不相等的模块
from django.db.models import Q
from authentication.api import base_func


# 服务器页面的级联选择框
def server_cascader(request):
    if request.method == 'GET':
        try:
            # 取出所有机房名称
            all_engine_name = {'value': 'engine_room', 'label': '机房', 'children': []}
            all_engine = EngineRoom.objects.all()
            for en in all_engine:
                all_engine_name['children'].append({'id': en.id,
                                                    'value': 'engine_room-'+str(en.id),
                                                    'label': en.name,
                                                    'disabled': True if en.is_del == '1' else False})

            # 取出所有项目名称
            all_project_name = {'value': 'project', 'label': '项目', 'children': []}
            all_project = Project.objects.all()
            for pro in all_project:
                all_project_name['children'].append({'id': pro.id,
                                                     'value': 'project-'+str(pro.id),
                                                     'label': pro.name,
                                                     'disabled': True if pro.is_del == '1' else False})

            # 取出所有操作系统名称
            all_os_name = {'value': 'os', 'label': '系统', 'children': []}
            all_os = Os.objects.all()
            for o in all_os:
                all_os_name['children'].append({'id': o.id,
                                                'value': 'os-'+str(o.id),
                                                'label': o.name,
                                                'disabled': True if o.is_del == '1' else False})

            # 取出所有机器类型名称
            all_machine_type_name = {'value': 'machine_type', 'label': '类型', 'children': []}
            all_type = MachineType.objects.all()
            for machine_type in all_type:
                all_machine_type_name['children'].append({'id': machine_type.id,
                                                          'value': 'machine_type-'+str(machine_type.id),
                                                          'label': machine_type.name,
                                                          'disabled': True if machine_type.is_del == '1' else False})

            data = {
                'status': 200,
                'msg': '取出级联选择框数据成功',
                'data': [all_engine_name, all_project_name, all_os_name, all_machine_type_name]
            }
            return JsonResponse(data)
        except:
            data = {
                'status': 500,
                'msg': '取出级联选择框数据失败',
            }
            return JsonResponse(data)
