from deploy.tools import ansible2_api

# resource = [
#     {'hostname': '122.112.225.26', 'ip': '122.112.225.26', 'port': '22', 'username': 'root', 'password': 'tst@hw@053', 'other_key1': 'other_value1'},
# ]
# ans = ansible2_api.ANSRunner(resource)
# # 这里的host_list必须在resource中
# ans.run_model(host_list=['122.112.225.26'], module_name='shell', module_args='top -bn1 |grep load')
# ad_hoc_result = ans.get_model_result()
# print(ad_hoc_result)

resource = [{
    'hostname': '192.168.1.150',
    'ip': '192.168.1.150',
    'port': '22',
    'username': 'root',
    'password': '111111',
    'CHANGE_ZONE': 'true',
    'CLOSE_SELINUX': 'true',
    'CLOSE_FIREWALL': 'false',
    'JAVA_PATH': '/usr/local'

}]
ans = ansible2_api.ANSRunner(resource)
# 这里传入的是playbook文件和全局参数
ans.run_playbook(playbook_path='server_init.yml', extra_vars=None)
playbook_result = ans.get_playbook_result()
print(playbook_result)