# 机房的增删改查类
from django.http import JsonResponse
from assets.models import EngineRoom
from authentication.api import base_func


# 查询和添加机房的方法
@base_func.login_check
def engine(request):
    # 查询机房列表方法
    if request.method == 'GET':
        engineroom_data = []

        try:
            all_engineroom = EngineRoom.objects.all()
            for engineroom in all_engineroom:
                engineroom_data.append({'id': engineroom.id,
                                        'name': engineroom.name,
                                        'location': engineroom.location,
                                        'create_time': engineroom.create_time,
                                        'text': engineroom.text,
                                        # 如果0,代表没删除返回False;如果1,代表删除了,返回True
                                        'is_del': False if engineroom.is_del == '0' else True})

            data = {
                'status': 200,
                'msg': '获取机房数据成功',
                'data': engineroom_data
            }
            return JsonResponse(data)
        except:
            data = {
                'status': 500,
                'msg': '从数据库中取数据失败',
            }
            return JsonResponse(data)

    # 添加机房方法
    elif request.method == 'POST':
        engine_name = request.POST.get('engine_name', 'ERROR')
        engine_location = request.POST.get('engine_location', 'ERROR')
        engine_text = request.POST.get('engine_text', 'ERROR')

        if engine_name == engine_location == engine_text == 'ERROR':
            data = {
                'status': 501,
                'msg': '从前端获取机房添加信息失败'
            }
            return JsonResponse(data)
        else:
            try:
                EngineRoom.objects.create(name=engine_name, location=engine_location, text=engine_text)
                data = {
                    'status': 200,
                    'msg': '添加机房成功'
                }
            except:
                data = {
                    'status': 502,
                    'msg': '在数据库中添加机房失败,请检查名称是否重复'
                }

            finally:
                return JsonResponse(data)


# 编辑机房的方法
@base_func.login_check
def engine_edit(request):
    # 编辑机房方法
    if request.method == 'POST':
        edit_engine_id = request.POST.get('engine_id', 'ERROR')
        edit_engine_name = request.POST.get('engine_name', 'ERROR')
        edit_engine_location = request.POST.get('engine_location', 'ERROR')
        edit_engine_text = request.POST.get('engine_text', 'ERROR')

        if edit_engine_id == edit_engine_name == edit_engine_location == edit_engine_text == 'ERROR':
            data = {
                'status': 500,
                'msg': '从前端获取机房修改信息失败'
            }
            return JsonResponse(data)

        else:
            try:
                engine_obj = EngineRoom.objects.get(id=edit_engine_id)
                engine_obj.name = edit_engine_name
                engine_obj.location = edit_engine_location
                engine_obj.text = edit_engine_text
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
def engine_delete(request):
    if request.method == 'POST':
        engine_id = request.POST.get('engine_id', 'ERROR')
        if engine_id == 'ERROR':
            data = {
                'status': 500,
                'msg': '从前端获取机房ID失败'
            }
            return JsonResponse(data)

        else:
            try:
                EngineRoom.objects.filter(id=engine_id).delete()
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
def engine_state(request):
    '''
    前端传过来的机房状态为true就代表要把这个is_del改成1,反之改为0
    :param request:
    :return:
    '''

    if request.method == 'POST':
        engine_id = request.POST.get('engine_id', 'ERROR')
        engine_state = request.POST.get('engine_state', 'ERROR')
        if engine_id == engine_state == 'ERROR':
            data = {
                'msg': '机房信息获取失败',
                'status': 500
            }
            return JsonResponse(data)
        try:
            # 注意这块!! 前端传过来的engine_state值是true/false,这个是字符串,不是布尔值!!!python里的是True,False
            # 所以需要以字符串的形式进行判断
            # 后面是三元表达式,成立返回前面的,不成立返回后面的
            EngineRoom.objects.filter(id=engine_id).update(is_del='1' if engine_state == 'true' else '0')

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