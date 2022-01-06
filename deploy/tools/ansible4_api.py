# 对应ansible版本为4.X ，卡在了playbook的回调函数不知道怎么调用，官方文档连个屁都没有，Google也搜不到，就停止这个版本的开发了
# 改成ansible2.4.1
import json,sys,os
import shutil

from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host, Group
#from ansible.module_utils.common.collections import ImmutableDict
from ansible import context
import ansible.constants as C

# 引入最外层文件夹的位置
#from cmdb.settings import BASE_DIR


# 复写资源清单管理类
# 重寫資源清單函數
class MyInventory():

    # 初始化方法，这里面接收一个resource资源对象格式为列表或字典
    # 列表格式如下：
    # [
    #      {'hostname': '192.168.1.1', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key1': 'other_value1'},
    #      {'hostname': '192.168.1.2', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key2': 'other_value2'},
    #      {'hostname': '192.168.1.3', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key3': 'other_value3'},
    #  ]
    # 字典格式如下:
    # {'group1':
    #     {'hosts':
    #         [
    #             {'hostname': '192.168.1.1', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key1': 'other_value1'},
    #             {'hostname': '192.168.1.2', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key2': 'other_value2'},
    #             {'hostname': '192.168.1.3', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'ssh_key': 'xxxxx', 'other_key3': 'other_value3'},
    #
    #         ],
    #      'vars':
    #             {
    #                 '组变量1': '组值1',
    #                 '组变量2': '组值2',
    #                 '组变量3': '组值2',
    #             },
    #     },
    #  'group2': {'hosts': [], 'vars': {}},
    #  'group3': {'hosts': [], 'vars': {}},
    # }

    def __init__(self, resource):
        self.resource = resource
        # 实例化数据源
        self.loader = DataLoader()
        # 实例化资源清单,先加载个文件进去,后面有需要在时候用方法添加
        self.inventory = InventoryManager(loader=self.loader, sources=['../conf/hostslist'])
        # 实例化变量管理器
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        # 把传进来的resource动态添加到资源清单中
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        # 添加主机组
        self.inventory.add_group(groupname)

        # 添加主机到主机组中
        for host in hosts:
            hostname = host.get("hostname")
            port = host.get("port")
            username = host.get("username")
            password = host.get("password")

            # 添加到主机组
            added_host = self.inventory.add_host(host=hostname, group=groupname, port=port)

            # 添加参数
            self.variable_manager.set_host_variable(host=added_host, varname='ansible_ssh_user', value=username)
            self.variable_manager.set_host_variable(host=added_host, varname='ansible_ssh_pass', value=password)

    def dynamic_inventory(self):
        # 判断传进来的resource是个列表
        if isinstance(self.resource, list):
            # 就把这个列表加入到默认组中添加到,并添加到资源清单
            self.add_dynamic_group(self.resource, 'default_group')

        # 如果resource是个字典
        elif isinstance(self.resource, dict):
            # 再遍历出字典添加到资源清单中
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


# ad-hoc模式的回調函數
class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    # 无法连接主机时的回调
    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    # 运行正常时的回调
    def v2_runner_on_ok(self, result,  *args, **kwargs):
        host = result._host
        self.host_ok[host.get_name()] = result

    # 执行失败时的回调
    def v2_runner_on_failed(self, result,  *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


# playbook模式的回调函數
class PlayBookResultsCollector(CallbackBase):
    CALLBACK_VERSION = 2.0
    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    # 正常运行
    def v2_runner_on_ok(self, result, *args, **kwargs):
        host = result._host
        self.task_ok[host.get_name()]  = result

    # 执行失败
    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.task_failed[host.get_name()] = result

    # 无法连接主机
    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.task_unreachable[host.get_name()] = result

    # 剧本跳过流程
    def v2_runner_on_skipped(self, result):
        host = result._host
        self.task_ok[host.get_name()] = result

    # playbook运行结果
    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok": t['ok'],
                                       "changed": t['changed'],
                                       "unreachable": t['unreachable'],
                                       "skipped": t['skipped'],
                                       "failed": t['failures']
                                   }


# 主函数
class ANSRunner(object):
    """
        resource： 传入的主机和变量
        redisKey: redis锁
        logID： 在MongoDB中的输出日志键
    """
    def __init__(self, resource, redisKey=None, logId=None, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}
        self.redisKey = redisKey
        self.logId = logId

    def __initializeData(self):
        context.CLIARGS = ImmutableDict(connection='smart',
                                        module_path=['/usr/share/ansible'],
                                        forks=5,
                                        become=None,
                                        become_method=None,
                                        become_user=None,
                                        check=False,
                                        diff=False,
                                        verbosity=0,
                                        syntax='yaml')

        self.loader = DataLoader()
        my_invent = MyInventory(self.resource)
        self.inventory = my_invent.inventory
        self.variable_manager = my_invent.variable_manager

    def run_model(self, host_list, module_name, module_args, gather_facts='no'):
        # 定义回调函数
        self.callback = ModelResultsCollector()

        # 定义执行队列
        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords,
            stdout_callback=self.callback,
        )

        """
        以ad-hoc模式运行
        module_name: ansible模块名称
        module_args: ansible模块参数
        gather_facts: 是否收集服务器信息，默认no，提高速度
        """
        play_source = dict(
                name="Ansible Play",
                hosts=host_list,
                gather_facts=gather_facts,
                tasks=[dict(action=dict(module=module_name, args=module_args))]
        )

        # 实例化play
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        try:
            tqm.run(play)
        # except Exception as err:
            # print(traceback.print_exc())
            # DsRedis.OpsAnsibleModel.lpush(self.redisKey,data=err)
            # if self.logId:AnsibleSaveResult.Model.insert(self.logId, err)
        finally:
            tqm.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        以playbook模式运行
        playbook_path： 剧本位置
        extra_vars： 附加全局变量，默认空
        """

        # 实例化回调函数
        self.callback = PlayBookResultsCollector()

        # 添加全局变量
        if extra_vars:
            self.variable_manager.extra_vars = extra_vars

        playbook = PlaybookExecutor(playbooks=[playbook_path,],
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    #options=self.options,
                                    passwords=self.passwords,

                                    )

        # playbook._tqm._stdout_callback = self.callback
        # playbook._tqm._stdout_callback
        # try:
            # if self.redisKey:self.callback = PlayBookResultsCollectorToSave(self.redisKey,self.logId)
            # 关闭第一次使用ansible连接客户端是输入命令
        # constants.HOST_KEY_CHECKING = False
        result = playbook.run()
        return result
        # except Exception as err:
        #     return err

    def get_model_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['success'][hostvisiable] = result._result


        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['failed'][hostvisiable] = result._result


        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.','_')
            self.results_raw['unreachable'][hostvisiable]= result._result

        # return json.dumps(self.results_raw)
        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped':{}, 'failed':{}, 'ok':{},"status":{},'unreachable':{},"changed":{}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        # for host, result in self.callback.task_changed.items():
        #     self.results_raw['changed'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result
        return self.results_raw


if __name__ == '__main__':
    # resource = [
    #              {"hostname": "192.168.8.119"},
    #              # {"hostname": "192.168.6.43"},
    #              # {"hostname": "192.168.1.233"},
    #              ]
    resource = [
         {'hostname': '192.168.1.150', 'ip': '192.168.1.150', 'port': '22', 'username': 'root', 'password': '111111', 'other_key1': 'other_value1'},
         {'hostname': '192.168.1.151', 'ip': '192.168.1.151', 'port': '22', 'username': 'root', 'password': '111111', 'other_key2': 'other_value2'},
         {'hostname': 'tomcat', 'ip': '192.168.1.152', 'port': '22', 'username': 'root', 'password': '111111', 'other_key3': 'other_value3'},
    ]
    mi = MyInventory(resource)
    print(mi.variable_manager.__dict__)
    # rbt = ANSRunner(resource)
    # Ansible Adhoc
    # rbt.run_model(host_list=['192.168.1.150', '192.168.1.151'], module_name='shell', module_args="ls /tmp")
    # data = rbt.get_model_result()
    # print(data)
    # Ansible playbook
    # print(rbt.run_playbook(playbook_path='./playbook.yml'))

    # rbt.run_model(host_list=[],module_name='yum',module_args="name=htop state=present")

