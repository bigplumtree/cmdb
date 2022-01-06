# 菜单类
from django.http import JsonResponse
from assets.models import Project
# 这个是判断不相等的模块
from django.db.models import Q
from authentication.api import base_func


# 项目的查看和添加方法
@base_func.login_check
def project(request):
    # 查询机房列表方法
    if request.method == 'GET':
        project_data = []

        try:
            all_project = Project.objects.all()
            for pro in all_project:
                project_data.append({'id': pro.id,
                                     'name': pro.name,
                                     'create_time': pro.create_time,
                                     'text': pro.text,
                                     # 如果0,代表没删除返回False;如果1,代表删除了,返回True
                                     'is_del': False if pro.is_del == '0' else True})

            data = {
                'status': 200,
                'msg': '获取项目数据成功',
                'data': project_data
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                'status': 500,
                'msg': '从数据库中取数据失败',
                'data': e
            }
            return JsonResponse(data)

    # 添加机房方法
    elif request.method == 'POST':
        project_name = request.POST.get('project_name', 'ERROR')
        project_text = request.POST.get('project_text', 'ERROR')

        if project_name == project_text == 'ERROR':
            data = {
                'status': 501,
                'msg': '从前端获取项目添加信息失败'
            }
            return JsonResponse(data)
        else:
            try:
                Project.objects.create(name=project_name, text=project_text)
                data = {
                    'status': 200,
                    'msg': '添加项目成功'
                }
            except:
                data = {
                    'status': 502,
                    'msg': '在数据库中添加项目失败,请检查名称是否重复'
                }

            finally:
                return JsonResponse(data)


# 编辑机房的方法
@base_func.login_check
def project_edit(request):
    # 编辑机房方法
    if request.method == 'POST':
        edit_project_id = request.POST.get('project_id', 'ERROR')
        edit_project_name = request.POST.get('project_name', 'ERROR')
        edit_project_text = request.POST.get('project_text', 'ERROR')

        if edit_project_id == edit_project_name == edit_project_text == 'ERROR':
            data = {
                'status': 500,
                'msg': '从前端获取项目修改信息失败'
            }
            return JsonResponse(data)

        else:
            try:
                engine_obj = Project.objects.get(id=edit_project_id)
                engine_obj.name = edit_project_name
                engine_obj.text = edit_project_text
                engine_obj.save()

                data = {
                    'status': 200,
                    'msg': '修改成功'
                }
            except Exception as E:
                data = {
                    'status': 501,
                    'msg': '数据库修改机房信息失败,请检查名称是否重复'
                }
            finally:
                return JsonResponse(data)


# 删除机房的方法
@base_func.login_check
def project_delete(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id', 'ERROR')

        if project_id == 'ERROR':
            data = {
                'status': 500,
                'msg': '从前端获取项目ID失败'
            }
            return JsonResponse(data)

        else:
            try:
                Project.objects.filter(id=project_id).delete()
                data = {
                    'status': 200,
                    'msg': '删除成功'
                }
            except:
                data = {
                    'status': 501,
                    'msg': '在数据库中删除机房失败,请假查该机房下是否有数据'
                }
            finally:
                return JsonResponse(data)


# 更改机房有效状态的方法
@base_func.login_check
def project_state(request):
    '''
    前端传过来的项目状态为true就代表要把这个is_del改成1,反之改为0
    :param request:
    :return:
    '''

    if request.method == 'POST':
        project_id = request.POST.get('project_id', 'ERROR')
        project_state = request.POST.get('project_state', 'ERROR')

        if project_id == project_state == 'ERROR':
            data = {
                'msg': '机房信息获取失败',
                'status': 500
            }
            return JsonResponse(data)
        try:
            # 注意这块!! 前端传过来的engine_state值是true/false,这个是字符串,不是布尔值!!!python里的是True,False
            # 所以需要以字符串的形式进行判断
            # 后面是三元表达式,成立返回前面的,不成立返回后面的
            Project.objects.filter(id=project_id).update(is_del='1' if project_state == 'true' else '0')

            data = {
                'msg': '状态修改完成',
                'status': 200
            }
        except Exception as error:
            data = {
                'msg': '状态修改失败',
                'status': 501,
            }
        finally:
            return JsonResponse(data)