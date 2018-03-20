<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>



### Environment Information



<table align="left">
<tr><td>System release version: </td><td>centos7.4</td></tr>
<tr><td>Zabbix version: </td><td>3.4.7</td></tr>
<tr><td>Installation type: </td><td >yum</td></tr>
</table>

### Resources
url: https://www.cnblogs.com/xiaolinstudy/p/7271861.html

### 1. 通过简单的配置自定义命令来监控一个进程是否存在


这里我们首先将UnsafeUserParameters的设置为1，该值默认为0,0表示不适用，1表示开启自定义脚本。
```bash
# vim  /etc/zabbix/zabbix_agentd.conf
UnsafeUserParameters=1
```

然后为开始添加自定义的key，key就是zabbix关键监控项，key的后面是一个监控命令或脚本。
```bash
# vim /etc/zabbix/zabbix_agentd.conf
UserParameter=proc.mysql,ps -ef|grep /usr/sbin/mysqld|grep -v grep|wc -l
```

- [x] Description

刚才的配置中，我们添加了一行UserParameter=proc.mysql,ps -ef|grep /usr/sbin/mysqld|grep -v grep|wc -l，</br>
其中，UserParameter是关键参数，我们要添加更多的自定义监控时也同样还有用到这个的，后就的proc.mysql是我们定义的一个key的名字，表示这个key就叫proc.mysql了，如果是监控http的进程我们可以写proc.http，方便我们通过key意识到内容是什么，而比如默认的key，net.tcp.listen，那这个名字就是识别网络的tcp端口的监听状况了。</br>
后面的逗号“,”是很关键的，用于分隔的，逗号后面的内容就是我们的命令或脚本的内容，本次的自定义监控中我们直接了一条命令来判断mysql服务的进程是否存在，如果存在，如果不存在，会返回0，如果存在，一般情况下回返回一个1.

#### Restart zabbix-agent service
完成配置后呢，我们就重启下服务。
```bash
[root@db1 ~]# systemctl restart zabbix-agent
```
#### Verification
然后，我们就可以去服务器端验证一下了，这里我直接先在命令行下验证,db1是一个hostname,会解析为我们客户单服务器ip。
```bash
[root@zabbix ~]# zabbix_get -s db1 -k proc.mysql
1
```
#### 在web端图形化的方式添加我们的自定义监控。

##### step1: 找到我们的目标主机
<img src=../images/22.jpg>
