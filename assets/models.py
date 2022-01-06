from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, null=False, verbose_name='菜单名称', help_text='菜单名称')
    pid = models.CharField(max_length=5, null=False, verbose_name='父菜单ID', help_text='父菜单ID')
    path = models.CharField(max_length=100, null=True, verbose_name='菜单路径', help_text='菜单路径')
    icon = models.CharField(max_length=100, null=True, verbose_name='菜单图标', help_text='菜单图标')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_assets_menu'
        verbose_name_plural = '菜单'


class EngineRoom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, null=False, verbose_name='机房名称', help_text='机房名称')
    location = models.CharField(max_length=100, null=True, verbose_name='机房位置', help_text='机房位置')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', help_text='创建时间')
    text = models.CharField(max_length=100, null=True, verbose_name='备注', help_text='备注')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_engine_room'
        verbose_name_plural = '机房'


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, null=False, verbose_name='项目名称', help_text='项目名称')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', help_text='创建时间')
    text = models.CharField(max_length=100, null=True, verbose_name='备注', help_text='备注')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_project'
        verbose_name_plural = '项目'


class Os(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, verbose_name='操作系统', help_text='操作系统', default='')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_os'
        verbose_name_plural = '操作系统'


class MachineType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, verbose_name='机器类型', help_text='机器类型：虚拟机或物理机', default='')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_machine_type'
        verbose_name_plural = '机器类型'


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    private_ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=False, verbose_name='内网IP地址', help_text='内网IP地址')
    public_ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, verbose_name='公网IP地址', help_text='公网IP地址')
    text = models.CharField(max_length=100, null=True, verbose_name='备注', help_text='备注')
    username = models.CharField(max_length=100, null=True, verbose_name='用户名', help_text='用户名', default='')
    password = models.CharField(max_length=100, null=True, verbose_name='密码', help_text='密码', default='')
    port = models.CharField(max_length=10, null=True, verbose_name='端口号', help_text='端口号', default='')
    os = models.ForeignKey(to="Os", to_field="id", on_delete=models.PROTECT, help_text='关联Os表')
    type = models.ForeignKey(to="MachineType", to_field="id", on_delete=models.PROTECT, help_text='关联机器类型表')
    engine_room = models.ForeignKey(to="EngineRoom", to_field="id", on_delete=models.PROTECT, help_text='关联机房表')
    project = models.ForeignKey(to="Project", to_field="id", on_delete=models.PROTECT, help_text='关联项目')
    is_del = models.CharField(max_length=1, null=False, default=0, verbose_name='有效状态', help_text='有效状态')

    def __str__(self):
        return self.private_ip_address

    class Meta:
        db_table = 'cmdb_server'
        verbose_name_plural = '服务器'


class Services(models.Model):
    id = models.AutoField(primary_key=True)
    belong_server = models.ForeignKey(to=Server, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255, null=False, verbose_name='服务名称', help_text='服务名称')
    service_version = models.CharField(max_length=100, null=True, verbose_name='服务版本', help_text='服务版本', default='/')
    service_port = models.CharField(max_length=100, null=True, verbose_name='服务端口', help_text='服务端口', default='/')
    service_dir = models.CharField(max_length=1000, null=True, verbose_name='安装目录', help_text='安装目录', default='/')
    owner = models.CharField(max_length=100, null=True, verbose_name='启动用户', help_text='启动用户', default='/')
    group = models.CharField(max_length=100, null=True, verbose_name='启动组', help_text='启动组', default='/')
    username = models.CharField(max_length=100, null=True, verbose_name='用户名', help_text='用户名', default='/')
    password = models.CharField(max_length=100, null=True, verbose_name='密码', help_text='密码', default='/')
    start_comm = models.CharField(max_length=1000, null=True, verbose_name='启动命令', help_text='启动命令', default='/')
    restart_comm = models.CharField(max_length=1000, null=True, verbose_name='重启命令', help_text='重启命令', default='/')
    enable_comm = models.CharField(max_length=1000, null=True, verbose_name='开机启动命令', help_text='开机启动命令', default='/')
    stop_comm = models.CharField(max_length=1000, null=True, verbose_name='停止命令', help_text='停止命令', default='/')
    text = models.CharField(max_length=1000, null=True, verbose_name='备注', help_text='备注')

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'cmdb_services'
        verbose_name_plural = '服务'


class ServiceConfig(models.Model):
    id = models.AutoField(primary_key=True)
    belong_service = models.ForeignKey(to=Services, on_delete=models.CASCADE)
    config_name = models.CharField(max_length=2555, null=False, verbose_name='配置文件名称', help_text='配置文件名称')
    config_hash = models.CharField(max_length=255, null=False, verbose_name='minio映射名称', help_text='minio映射名称')
    file_size = models.CharField(max_length=255, null=False, default='0', verbose_name='配置文件大小', help_text='配置文件大小')
    file_type = models.CharField(max_length=255, null=True, verbose_name='配置文件格式', help_text='配置文件格式')
    file_charset = models.CharField(max_length=255, null=True, verbose_name='配置文件字符集', help_text='配置文件字符集')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='修改时间', help_text='修改时间')

    def __str__(self):
        return self.config_name

    class Meta:
        db_table = 'cmdb_config_file'
        verbose_name_plural = '配置文件'


class ServerRate(models.Model):
    id = models.AutoField(primary_key=True)
    belong_server = models.ForeignKey(to=Server, on_delete=models.CASCADE)
    cpu_rate = models.CharField(max_length=255, null=True, verbose_name='CPU使用率', help_text='CPU使用率')
    mem_rate = models.CharField(max_length=255, null=True, verbose_name='内存使用率', help_text='内存使用率')
    disk_rate = models.CharField(max_length=2555, null=True, verbose_name='磁盘使用率', help_text='磁盘使用率')
    update_time = models.DateTimeField(auto_now=True, null=True, verbose_name='上次更新时间', help_text='上次更新时间')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'cmdb_server_rate'
        verbose_name_plural = '服务器资源信息'


# class Auth(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=100, null=False, verbose_name='用户名', help_text='用户名')
#     password = models.CharField(max_length=100, null=False, verbose_name='密码', help_text='密码')
#     is_admin = models.CharField(max_length=1, default=0, null=False, verbose_name='管理员', help_text='管理员')
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         db_table = 'cmdb_auth'
#         verbose_name_plural = '登录认证'
