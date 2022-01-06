from django.http import JsonResponse
from authentication.models import CmdbAuth


# 登录认证装饰器
def login_check(func):
    def inner(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token == None:
            # 如果取不到token,返回401 没有认证
            return JsonResponse({'status': 401, 'msg': 'No Authorization'})
        else:
            try:
                user = CmdbAuth.objects.get(token=token)
                is_admin = user.is_admin
                is_del = user.is_del
                if is_del == '0':
                    # 如果从数据库中得到这个token没有失效,就继续执行后面的方法
                    return func(request, *args, **kwargs)
                else:
                    # 如果用户失效,返回403, 权限不足
                    return JsonResponse({'status': 403, 'msg': 'Permissions Deny'})
            except:
                # 如果从数据库中取回数据失败,就返回非法用户
                return JsonResponse({'status': 417, 'msg': 'Illegal User'})
    return inner


# 登陆认证函数
def login(request):
    # 登陆认证别返回token
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username == password == None:
            data= {
                'status': 501,
                'msg': '从前端获取用户名密码失败'
            }
            return JsonResponse(data)

        else:
            try:
                user = CmdbAuth.objects.get(username=username, password=password)
                token = user.token
                data = {
                    'status': 200,
                    'msg': '认证成功',
                    'data': {'token': token}
                }
            except:
                data = {
                    'status': 403,
                    'msg': '用户名或密码错误',
                }
            finally:
                return JsonResponse(data)
