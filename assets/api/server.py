# 菜单类
import ast
from django.http import JsonResponse
from assets.models import EngineRoom, Project, Os, MachineType, Server, ServerRate
# 这个是判断不相等的模块
from django.db.models import Q
from authentication.api import base_func
import paramiko


# 获取服务器列表
@base_func.login_check
def server(request):
    # 查询服务器列表方法
    if request.method == 'GET':
        query = request.GET.get('query', None)

        # 这里定义的字典是给orm过滤条件用的，因为不知道前端传过来的级联选择器带哪些参数
        # 可能会遇到有些选项没有选中，有些选项被选中的情况
        # 那么在orm过滤条件的时候，无法把过滤条件写死在代码中
        # orm filter提供以字典格式的传参，传入后使用**解开赋值
        # 这个字典就是传参用的
        # 字典的key就是orm filter中的过滤条件
        # 字典的value就是orm filter中的过滤值
        query_dict = {}

        # 目前这里只定义了四种过滤规则,如果后期前端又添加了新的过滤规则,这块还需要手动添加其他的过滤
        if query is not None:
            en = []
            pro = []
            os = []
            ty = []
            # 上面定义的四个列表是接收前端传参用的
            # 前端传过来的Key是engine_room-，XXXX-，xxxx-
            # 前端传过来的value就是各数据库中的id值
            # 下面的循环就是在取orm查询时的外键ID
            for value in query.split(','):
                if value.startswith('engine_room-'):
                    en.append(value.strip('engine_room-'))

                elif value.startswith('project-'):
                    pro.append(value.strip('project-'))

                elif value.startswith('os-'):
                    os.append(value.strip('os-'))

                elif value.startswith('machine_type-'):
                    ty.append(value.strip('machine_type-'))

            # 这里将各ID值列表放入字典中，如果列表没空就代表前端没选这个选项，不再给字典添加这个参数
            if en: query_dict['engine_room__id__in'] = en
            if pro: query_dict['project__id__in'] = pro
            if os: query_dict['os__id__in'] = os
            if ty: query_dict['type__id__in'] = ty

        current_pag = int(request.GET.get('current_pag', 1))
        pagesize = int(request.GET.get('pagesize', 10))

        # 分页功能，起始位置和偏移量，相当于sql中的offset和limit
        start_row = (current_pag - 1) * pagesize
        end_row = current_pag * pagesize
        server_data = []
        try:
            # 根据过滤条件返回服务器的总数，前端的分页框需要这个
            total = Server.objects.filter(**query_dict).count()
            # 根据过滤条件使用offset和limit组成的分页查询
            all_server = Server.objects.filter(**query_dict)[start_row:end_row]

            for ser in all_server:
                server_data.append({
                    'id': ser.id,
                    'private_ip_address': ser.private_ip_address,
                    'public_ip_address': ser.public_ip_address,
                    'text': ser.text,
                    'username': ser.username,
                    'password': ser.password,
                    'port': ser.port,
                    'os': ser.os.name,
                    'os_id': ser.os.id,
                    'type': ser.type.name,
                    'type_id': ser.type.id,
                    'engine_room': ser.engine_room.name,
                    'engine_room_id': ser.engine_room.id,
                    'project': ser.project.name,
                    'project_id': ser.project.id,
                    'is_del': ser.is_del
                })
            data = {
                'msg': '获取服务器列表成功',
                'status': 200,
                'data': {
                    'data': server_data,
                    'total': total
                }
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                'msg': '获取服务器列表失败',
                'status': 500,
            }
            return JsonResponse(data)

    # 添加服务器方法
    if request.method == 'POST':
        private_ip = request.POST.get('private_ip', 'ERROR')
        public_ip = request.POST.get('public_ip', 'ERROR')
        username = request.POST.get('username', 'ERROR')
        password = request.POST.get('password', 'ERROR')
        port = request.POST.get('port', 'ERROR')
        engine = request.POST.get('engine', 'ERROR')
        project = request.POST.get('project', 'ERROR')
        os = request.POST.get('os', 'ERROR')
        machine_type = request.POST.get('machine_type', 'ERROR')
        text = request.POST.get('text', 'ERROR')

        if private_ip == public_ip == username == password == port == engine == project == os == machine_type == text == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 501
            }
            return JsonResponse(data)
        else:
            try:
                s = Server.objects.create(
                    private_ip_address=private_ip,
                    public_ip_address=public_ip,
                    username=username,
                    password=password,
                    port=port,
                    engine_room_id=engine,
                    project_id=project,
                    os_id=os,
                    type_id=machine_type,
                    text=text
                )

                ServerRate.objects.create(
                    belong_server_id = s.id,
                    cpu_rate = '',
                    mem_rate = '',
                    disk_rate = ''
                )

                data = {
                    'msg': '添加成功',
                    'status': 200
                }
                return JsonResponse(data)
            except Exception as e:

                print(e)
                data = {
                    'msg': '在数据库中添加失败',
                    'status': 500
                }
                return JsonResponse(data)


# 编辑服务器接口
@base_func.login_check
def server_edit(request):
    # 编辑服务器方法
    if request.method == 'POST':
        server_id = request.POST.get('server_id', 'ERROR')
        private_ip = request.POST.get('private_ip', 'ERROR')
        public_ip = request.POST.get('public_ip', 'ERROR')
        username = request.POST.get('username', 'ERROR')
        password = request.POST.get('password', 'ERROR')
        port = request.POST.get('port', 'ERROR')
        engine = request.POST.get('engine', 'ERROR')
        project = request.POST.get('project', 'ERROR')
        os = request.POST.get('os', 'ERROR')
        machine_type = request.POST.get('machine_type', 'ERROR')
        text = request.POST.get('text', 'ERROR')

        if server_id == private_ip == public_ip == username == password == port == engine == project == os == machine_type == text == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 501
            }
            return JsonResponse(data)
        else:
            try:
                s = Server.objects.get(id=server_id)
                s.private_ip_address = private_ip
                s.public_ip_address = public_ip
                s.username = username
                s.password = password
                s.port = port
                s.engine_room_id = engine
                s.project_id = project
                s.os_id = os
                s.type_id = machine_type
                s.text = text
                s.save()

                data = {
                    'msg': '修改成功',
                    'status': 200
                }
                return JsonResponse(data)
            except Exception as e:
                print(e)
                data = {
                    'msg': '在数据库中修改失败',
                    'status': 500
                }
                return JsonResponse(data)


# 删除服务器接口
@base_func.login_check
def server_delete(request):
    if request.method == 'POST':
        server_id = request.POST.get('server_id', 'ERROR')
        if server_id == 'ERROR':
            data = {
                'msg': '从前端获取参数失败',
                'status': 501
            }
            return JsonResponse(data)
        else:

            try:
                Server.objects.filter(id=server_id).delete()
                data = {
                    'msg': '删除成功',
                    'status': 200
                }
                return JsonResponse(data)
            except:
                data = {
                    'msg': '从数据库中删除失败',
                    'status': 500
                }
                return JsonResponse(data)


# 服务器echart图接口
@base_func.login_check
def server_echart(request):
    if request.method == 'GET':
        echart_list = []
        engine_dict = {}
        try:
            # 先把第一层的机房名称取出来放到一个字典里
            all_engine = EngineRoom.objects.values('name')
            for en in all_engine:
                engine_dict[en['name']] = []

            # 再取出所有机器，根据机器的机房外键，分别存放到不同的机房字典里
            # print(engine_dict)
            all_server = Server.objects.values('engine_room__name', 'public_ip_address', 'text')
            for ser in all_server:
                # print(ser['engine_room__name'], ser['private_ip_address'])
                # echart树图的value必须是数字，其他类型不显示
                #engine_dict[ser['engine_room__name']].append({'name': ser['private_ip_address'], 'value': ser['text']})
                engine_dict[ser['engine_room__name']].append({'name': ser['public_ip_address'].ljust(16) + ser['text']})

            # print(engine_dict)

            # 填充echart所需要的数据形式
            for name, value in engine_dict.items():
                echart_list.append({'name': name, 'children': value})

            # print(echart_list)

            data = {
                'status': 200,
                'data': {
                    'name': 'TST',
                    'children': echart_list
                }
            }
            return JsonResponse(data)

        except:

            data = {
                'status': 500,
                'message': '组装echart数据失败'
            }
            return JsonResponse(data)


# 获取服务器硬件信息接口
# @base_func.login_check
def server_rate(request):
    if request.method == 'GET':
        server_id = request.GET.get('server_id', 'ERROR')
        server_ip = request.GET.get('server_ip', 'ERROR')
        server_username = request.GET.get('server_username', 'ERROR')
        server_password = request.GET.get('server_password', 'ERROR')
        server_connport = request.GET.get('server_connport', ' ERROR')
        refresh = request.GET.get('refresh', '0')

        if server_id == server_ip == server_username == server_password == server_connport == refresh == 'ERROR':
            data = {
                'status': 501,
                'msg': '从前端获取信息失败'
            }
            return JsonResponse(data)

        # 如果不是手动刷新，就从数据库获取这个记录，如果数据库没有查询到，就返回指定字符
        elif refresh == '0':
            try:
                s = ServerRate.objects.get(belong_server_id=server_id)
                # 数据库中存的格式是'['1','2','3']' ,字符串格式的列表，需要把他转成列表再去切片
                # 如果转成列表的时候出现错误，代表数据库中存储的可能有问题
                cpu2mysql = ast.literal_eval(s.cpu_rate)
                memory2mysql = ast.literal_eval(s.mem_rate)
                disk2mysql = ast.literal_eval(s.disk_rate)
                update_time = s.update_time
                data = {
                    'status': 200,
                    'data': {
                        'cpu_rate_1min': cpu2mysql[0],
                        'cpu_rate_5min': cpu2mysql[1],
                        'cpu_rate_15min': cpu2mysql[2],
                        'total_memory': memory2mysql[0],
                        'available_memory': memory2mysql[1],
                        'memory_rate': memory2mysql[2],
                        'disk_rate': disk2mysql,
                        'update_time': update_time
                        }
                }
                return JsonResponse(data)
            except SyntaxError as e:
                data = {
                    'status': 503,
                    'msg': '数据库中存储的格式不对，无法解析'
                }
                return JsonResponse(data)
            except Exception:
                data = {
                    'status': 505,
                    'msg': '发生其他错误，无法解析'
                }
                return JsonResponse(data)

        # 如果是手动点的刷新，就连接服务器去请求查询，之后在存数据库一份
        elif refresh == '1':
            from cmdb.settings import CPU_UTILIZATION_RATE, MEM_UTILIZATION_RATE, DISK_UTILIZATION_RATE
            try:
                ssh_server = paramiko.SSHClient()
                ssh_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_server.connect(hostname=server_ip,
                                   port=server_connport,
                                   username=server_username,
                                   password=server_password,
                                   timeout=5)
                cpu_stdin, cpu_stdout, cpu_stderr = ssh_server.exec_command(CPU_UTILIZATION_RATE)
                mem_stdin, mem_stdout, mem_stderr = ssh_server.exec_command(MEM_UTILIZATION_RATE)
                disk_stdin, disk_stdout, disk_stderr = ssh_server.exec_command(DISK_UTILIZATION_RATE)

                # 存入MySQL的格式，都是列表形式
                cpu2mysql = cpu_stdout.read().decode('utf-8').split(',')
                memory2mysql = mem_stdout.read().decode('utf-8').split(',')
                disk2mysql = disk_stdout.read().decode('utf-8').split(';')[0:-1]

                ssh_server.close()

            except:
                data = {
                    'status': 505,
                    'msg': '连接服务器失败'
                }
                return JsonResponse(data)

            try:
                s = ServerRate.objects.get(belong_server_id=server_id)
                s.cpu_rate = cpu2mysql
                s.mem_rate = memory2mysql
                s.disk_rate = disk2mysql
                s.save()
                update_time = s.update_time

                data = {
                    'status': 200,
                    'data': {
                        'cpu_rate_1min': cpu2mysql[0],
                        'cpu_rate_5min': cpu2mysql[1],
                        'cpu_rate_15min': cpu2mysql[2],
                        'total_memory': memory2mysql[0],
                        'available_memory': memory2mysql[1],
                        'memory_rate': memory2mysql[2],
                        'disk_rate': disk2mysql,
                        'update_time': update_time
                        }
                }
                return JsonResponse(data)
            except:
                data = {
                    'status': 502,
                    'msg': '获取服务器信息成功，但是存储数据库时发生错误',
                }
                return JsonResponse(data)
