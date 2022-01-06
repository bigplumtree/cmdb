# 1.文件描述
ansible4_api：这个工具类文件无法使用，被卡在playbook模式的回调函数，我找不到怎么把回调函数给运行模块

ansible2_api：这个工具类文件可以正常使用

# 2.引入方法

```
from xxxx.xxxx import ansible2_api
```


# 3.调用方法
> **ad-hoc模式运行**

```
  ans = ansible2_api.ANSRunner(resource)
  # 这里的host_list必须在resource中
  ans.run_model(host_list=['192.168.1.150'], module_name='shell', module_args='ls /tmp')
  ad_hoc_result = ans.get_model_result()
  print(ad_hoc_result)
```


> **playbook模式运行**

```
  ans = ansible2_api.ANSRunner(resource) 
  # 这里传入的是playbook文件和全局参数
  ans.run_playbook(playbook_path='test.yml', extra_vars=None)
  playbook_result = ans.get_playbook_result()
  print(playbook_result)
```


# 4.资源参数：参数分类两种类型

> **·列表：以列表方式，会将传入的主机都放到default_group组里面**

```
[
    {'hostname': '192.168.1.1', 'ip': '192.168.1.1', 'port': '22', 'username': 'root', 'password': '123456', 'other_key1': 'other_value1'},
    {'hostname': '192.168.1.2', 'ip': '192.168.1.2', 'port': '22', 'username': 'root', 'password': '123456', 'other_key2': 'other_value2'}, 
    {'hostname': '192.168.1.3', 'ip': '192.168.1.3', 'port': '22', 'username': 'root', 'password': '123456', 'other_key3': 'other_value3'},
]
```

> 必传参数：

| header1 | header2 |
| ------- | ------- |
| hostname| 主机名称，格式不限        |
| ip      | 需要操控的主机IP|
| port    | 需要操控的主机端口|
| username| 需要操控的主机用户名|
| password| 需要操控的主机密码|
  
> 可选参数：

| header1 | header2 |
| ------- | ------- |
|  key1   | value1  |
| key2    | value2  |


> **·字典：以字典方式，传入的主机会和组相对应**

```
{
    'group1':
        {
            'hosts':
                [
                    {'hostname': '192.168.1.1', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'other_key1': 'other_value1'},
                    {'hostname': '192.168.1.2', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'other_key2': 'other_value2'},
                    {'hostname': '192.168.1.3', 'ip': '', 'port': '22', 'username': 'root', 'password': '123456', 'other_key3': 'other_value3'},
                ],
            'vars':
                {
                    '组变量1': '组值1',
                    '组变量2': '组值2',
                    '组变量3': '组值2',
                },
        },
    'group2': 
        {
            'hosts': [],
            'vars': {}
        },
    'group3':
        {
            'hosts': [],
            'vars': {}
        },
}
```


> 必传参数：

| header1 | header2 |
| ------- | ------- |
| hostname| 主机名称，格式不限        |
| ip      | 需要操控的主机IP|
| port    | 需要操控的主机端口|
| username| 需要操控的主机用户名|
| password| 需要操控的主机密码|
  
> 可选参数：

| header1 | header2 |
| ------- | ------- |
|  key1   | value1  |
| key2    | value2  |


# 5.playbook格式

```
---                       #固定格式
- hosts: all   #定义需要执行主机
  remote_user: root       #远程用户
  vars:                   #定义变量
    http_port: 8088       #变量

  tasks:                             #定义一个任务的开始
    - name: create new file          #定义任务的名称
      shell: ls /tmp   #调用模块，具体要做的事情
```


