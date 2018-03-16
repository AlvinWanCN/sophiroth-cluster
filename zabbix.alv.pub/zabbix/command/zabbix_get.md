<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


## Introduce zabbix_get command function


reference url:http://blog.csdn.net/chuang3344/article/details/74081682


- [x] system.uname

返回主机相信信息.字符串
```bash
[root@zabbix ~]# zabbix_get -s 192.168.127.52 -k 'system.uname'
Linux db1.alv.pub 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64
```

- [x] system.hostname

system.hostname[<type>]
返回主机名字符串

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'system.hostname'
db2.alv.pub

```

system.cpu.num[<type>]

CPU数量处理器个数type - 可用值: online (默认值), max范例: system.cpu.num

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'system.cpu.num'
4
```


system.uptime

系统运行时长(秒)多少秒使用s/uptime来获取

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'system.uptime'
69695
```

system.users.num

登陆用户数量多少用户agent使用who命令获取

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'system.users.num'
2

```


vm.memory.size[<mode>]

内存大小字节或百分比
```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k vm.memory.size[free]
840826880
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k vm.memory.size[used]
3117232128
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k vm.memory.size[total]
3958075392
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k vm.memory.size[available]
3118415872

```


agent.hostname

返回被监控端名称(字符串)

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'agent.hostname'
db2.alv.pub

```



kernel.maxfiles

系统支持最大的open files整数

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'kernel.maxfiles'
379643

```


agent.version

zabbix agent版本字符串

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'agent.version'
3.4.7

```

kernel.maxproc

系统支持最大的进程数量整数
```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'kernel.maxproc'
131072

```

net.tcp.listen[port]</br>
检测端口是否开启0 – （not listen） 1 –  in LISTEN stateport</br>
示例: net.tcp.listen[80]</br>

```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'net.tcp.listen[22]'
1
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'net.tcp.listen[232]'
0

```


net.tcp.port[<ip>,port]</br>
是否可以连接到指定的TCP端口0 – cannot connect 1 – can connect</br>
   ip - IP地址(默认是 127.0.0.1)</br>
   port - 端口</br>
范例: net.tcp.port[,80] 检测web服务器端口是否运行中</br>
```bash
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'net.tcp.port[,80]'
0
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'net.tcp.port[,3306]'
1
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'net.tcp.port[,22]'
1

```
```bash

net.tcp.service[service,<ip>,<port>]
检测服务是否开启，并且端口可用0 – 服务挂了 1 – 服务运行中
    service - 如下:ssh, ntp, ldap, smtp, ftp, http, pop, nntp,imap, tcp, https, telnet
    ip - IP地址 (默认127.0.0.1)
    port - 端口 (默认情况为标准端口号)
示例key: net.tcp.service[ftp,,45]


[root@zabbix ~]# zabbix_get -s db2.alv.pub -k net.tcp.service[ftp,,45]
0

```



vfs.fs.size[{#FSNAME},used]

查看磁盘使用率
```bash

[root@zabbix ~]# zabbix_get -s db2.alv.pub -k  "vfs.fs.size[/opt,used]"  
3297542144
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k  "vfs.fs.size[/opt,total]"  
19862126592
```
