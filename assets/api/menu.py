# 菜单类
from django.http import JsonResponse
from assets.models import Menu
# 这个是判断不相等的模块
from django.db.models import Q
from authentication.api import base_func
from authentication.models import CmdbAuth


# 获取菜单列表
# todo 1.这次获取列表的时候查询了两次数据库,需要改成查询一次
#      2.当父菜单的节点状态为删除,子菜单没有删除时,会报错
@base_func.login_check
def get_menus(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION', None)
        parent_menu_data = {}

        try:
            is_admin = CmdbAuth.objects.get(token=token).is_admin
            if is_admin == '1':
                # 取出所有父节点
                all_parent_menu = Menu.objects.filter(pid=0, is_del=0)
                # 取出所有子节点,~Q就是取反的意思
                all_children_menu = Menu.objects.filter(~Q(pid=0), is_del=0)
            else:
                # 因为没有做权限管理，这里只是不让非管理员用户看到资产列表界面，并没有对其使用接口调用方式去做限制，
                # 只是不让在网页上看到资产列表而已，后面有时间会把权限加上
                all_parent_menu = Menu.objects.filter(~Q(id=1), pid=0, is_del=0)
                # pid=0是父节点，pid=1是资产管理子节点
                all_children_menu = Menu.objects.filter(~Q(pid=0), ~Q(pid=1), is_del=0)

            for parent_menu in all_parent_menu:
                # 把所有父节点以字典的形式存起来,为了方便在添加子节点的时候容易找到父节点
                parent_menu_data[str(parent_menu.id)] = ({'id': parent_menu.id,
                                                          'name': parent_menu.name,
                                                          'path': parent_menu.path,
                                                          'icon': parent_menu.icon,
                                                          'children': []})

            for children_menu in all_children_menu:
                # 找到所有子节点,根据子节点中的pid值添加到父节点的children列表中
                parent_menu_data[children_menu.pid]['children'].append({'id': children_menu.id,
                                                                        'name': children_menu.name,
                                                                        'path': children_menu.path,
                                                                        'icon': children_menu.icon,
                                                                        })

            # 取出列表
            menu_data = list(parent_menu_data.values())

            # 组数据
            data = {
                'msg': '成功',
                'status': '200',
                'data': menu_data
            }
            # 正确时返回
            return JsonResponse(data)

        except Exception as error:

            # 组数据
            data = {
                'msg': '从数据库中获取菜单列表失败',
                'status': '500',
                'data': error
            }
            # 错误时返回
            return JsonResponse(data)


