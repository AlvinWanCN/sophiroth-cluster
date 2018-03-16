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
[root@zabbix ~]# zabbix_get -s db2.alv.pub -k 'vm.memory.size'
3958075392

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