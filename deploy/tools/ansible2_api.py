#!/usr/bin/env python
# -*- coding=utf-8 -*-
# ansible模块：2.4.1
# python版本：3.6.8

import json,sys,os, time
import random
import shutil
import ansible.constants as C
from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group


class MyInventory():
    # 初始化
    def __init__(self, resource):
        self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=[''])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.dynamic_inventory()

    # 添加前端传过来的值
    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        # 添加组
        self.inventory.add_group(groupname)
        # 添加组变量（我感觉这一段没有用）
        my_group = Group(name=groupname)
        if groupvars:
            for key, value in groupvars.items():
                my_group.set_variable(key, value)

        # 添加主机变量
        for host in hosts:
            # 设置主机连接变量
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            my_host = Host(name=hostname, port=hostport)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_host',value=hostip)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_pass',value=password)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_port',value=hostport)
            self.variable_manager.set_host_variable(host=my_host,varname='ansible_ssh_user',value=username)

            # 设置其他主机变量
            for key, value in host.items():
                if key not in ["hostname", "port", "username", "password"]:
                    self.variable_manager.set_host_variable(host=my_host,varname=key,value=value)

            # 添加到组
            self.inventory.add_host(host=hostname,group=groupname,port=hostport)

    def dynamic_inventory(self):
        # 判断传过来的是列表还是字典
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


# ad-hoc模式的回调函数
# 日志里都有什么可以通过result.__dict__查看
class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now
        self.host_unreachable[host] = result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now
        self.host_ok[host] = result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now
        self.host_failed[host] = result


# 剧本模式的回调函数
# 日志里都有什么可以通过result.__dict__查看
class PlayBookResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now
        self.task_ok[host] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(result.__dict__)
        host = result._host.get_name() + '==>' + now
        self.task_failed[host] = result

    def v2_runner_on_unreachable(self, result):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now
        self.task_unreachable[host] = result

    def v2_runner_on_skipped(self, result):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        host = result._host.get_name() + '==>' + now + str(random.randint(1, 10000))
        self.task_skipped[host] = result

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


class ANSRunner(object):
    """
    真正的运行函数
    """
    def __init__(self,resource, redisKey=None, logId=None, *args, **kwargs):
        self.resource = resource
        self.passwords = None
        self.__initializeData()
        self.results_raw = {}
        self.redisKey = redisKey
        self.logId = logId

    def __initializeData(self):
        """ 初始化ansible """
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                listtasks=False, listtags=False, syntax=False, diff=True)

        myinvent = MyInventory(self.resource)
        self.loader = myinvent.loader
        self.inventory = myinvent.inventory
        self.variable_manager = myinvent.variable_manager

    def run_model(self, host_list, module_name, module_args):
        """
        以ad-hoc模式运行
        host_list： 需要运行的主机ip列表
        module_name: ansible模块名称
        module_args: ansible模块参数
        """
        # 实例化回调函数
        self.callback = ModelResultsCollector()

        play_source = dict(
                name="Ansible Play",
                hosts=host_list,
                gather_facts='no',
                tasks=[dict(action=dict(module=module_name, args=module_args))]
        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
        # else:self.callback = ModelResultsCollector()

        import traceback
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
                    stdout_callback=self.callback,
            )
            tqm._stdout_callback = self.callback
            # 关闭第一次使用ansible连接客户端需要输入yes/no
            constants.HOST_KEY_CHECKING = False
            tqm.run(play)
        except Exception as err:
            print(traceback.print_exc())
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
        playbook_path： playbook位置
        """
        # 实例化回调函数
        self.callback = PlayBookResultsCollector()
        try:
            # if self.redisKey:self.callback = PlayBookResultsCollectorToSave(self.redisKey,self.logId)
            # 如果有传过来的全局变量，就加进去
            if extra_vars:
                self.variable_manager.extra_vars = extra_vars

            playbook = PlaybookExecutor(
                playbooks=[playbook_path],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )

            # 指定回调函数
            playbook._tqm._stdout_callback = self.callback

            # 关闭第一次使用ansible连接客户端是输入命令
            constants.HOST_KEY_CHECKING = False
            playbook.run()
        except Exception as err:
            return False

    # 获取ad-hoc模式运行的返回结果
    def get_model_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result

        return self.results_raw

    # 获取以playbook模式运行的返回结果
    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result.task_name

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = '\n' \
                                               + '失败条目：' \
                                               + result._task.get_name() \
                                               + '\n' \
                                               + result._result.get('msg') \
                                               + '\n' \
                                               + '控制台输出：' \
                                               + '\n' \
                                               + result._result.get('stdout') \


        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        # for host, result in self.callback.task_changed.items():
        #     self.results_raw['changed'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result._task

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result

        return self.results_raw
