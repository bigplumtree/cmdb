import paramiko


cpu_utilization_rate = 'top -bn1 | grep load | awk \'{printf \"{ONE_MIN:%.2f,FIVE_MIN:%.2f,FIFTEEN_MIN:%.2f}\", $(NF-2),$(NF-1),$(NF-0)}\''
mem_utilization_rate = 'free -m | awk \'NR==2{printf \"{MEM_TOTAL:%s,MEM_AVAILABLE:%s}\",$2,$7 }\''
disk_utilization_rate = 'df -m -t ext2 -t ext3 -t ext4 -t xfs | grep -vE \'^Filesystem|tmpfs|cdrom\'  | awk \'{ printf \"{DISK_TOTAL:%.2f,DISK_AVAILABLE:%.2f},\",($2/1024),($4/1024),$5 }\''
ssh_server = paramiko.SSHClient()
ssh_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_server.connect(hostname='122.112.225.26', port=22, username='root', password='tst@hw@053',timeout=5)
cpu_stdin, cpu_stdout, cpu_stderr = ssh_server.exec_command(cpu_utilization_rate)
mem_stdin, mem_stdout, mem_stderr = ssh_server.exec_command(mem_utilization_rate)
disk_stdin, disk_stdout, disk_stderr = ssh_server.exec_command(disk_utilization_rate)

c = cpu_stdout.read().decode('utf-8')
m = mem_stdout.read().decode('utf-8')
d = disk_stdout.read().decode('utf-8')

print(c,m,d)
ssh_server.close()
