<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>



## Environment Information



<table align="left">
<tr><td>System release version: </td><td>centos7.4</td></tr>
<tr><td>Zabbix version: </td><td>3.4.7</td></tr>
<tr><td>Installation type: </td><td >yum</td></tr>
</table>

## Resources
url: https://www.cnblogs.com/xiaolinstudy/p/7271861.html


## Catelog

[1.简单命令创建监控项](#通过简单的配置自定义命令来监控一个进程是否存在)</br>
[2.通过脚本传递参数方式自定义监控](#通过脚本传递参数方式自定义监控)</br>


## Content
### 通过简单的配置自定义命令来监控一个进程是否存在


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

##### step1: 找到我们的目标主机,点击items
<img src=../images/22.jpg>

##### step2: 点击Create item
<img src=../images/23.jpg>

##### step3: 配置item。
<img src=../images/24.jpg>

那现在我就将这个item配置好了。

<img src=../images/25.jpg>

##### step4: 查看监控到的数据
<img src=../images/26.jpg>

但是现在还没有告警功能，所以我们去创建一个触发器，一个Trigger

##### step5: 创建一个trigger

<img src=../images/27.jpg>

##### step6： 配置trigger
这里我们填写好name，选择Severity这里的内容，我们选择disaster，表示这个是严重的。

然后我们先点击Expression这里的add

<img src=../images/28.jpg>

选择select

<img src=../images/29.jpg>

找到我们刚才配置的mysql进程监控的item名

<img src=../images/30.jpg>

然后配置表达式，这里我们配置为最新的值是0的时候我们告警。

<img src=../images/31.jpg>

然后完成配置，确认添加，创建时最下面是add，再次点进去add会变成update。


<img src=../images/32.jpg>

然后完成配置了。

##### step7: 验证触发器
这里我们关闭被监控服务器的mysql服务
```bash
[root@db1 ~]# systemctl stop mysql
```

我们查询最新数据和图表，可以看到该item已有我们刚才设置的触发器了，然后最新的值是0了。

<img src=../images/33.jpg>

现在，我们也收到触发器触发的告警了，已收到邮件

<img src=../images/34.jpg>

<img src=../images/35.jpg>

重启启动mysql服务

```bash
[root@db1 ~]# systemctl start mysql
```

然后收到邮件通知，mysql挂掉的问题已经恢复。

<img src=../images/36.jpg>


### 通过脚本传递参数方式自定义监控

#### 编写脚本

这里我在编写了一个脚本，名为/root/detect_proc.py, 该脚本接受一个参数，$1,同时我给这个脚本执行权限。
```bash
[root@db1 ~]# mkdir -p /etc/zabbix/scripts
[root@db1 ~]# vim /etc/zabbix/scripts/detect_proc.py
#!/usr/bin/python
import sys,os
processes_name=sys.argv[1]

os.system('ps -ef|grep %s|grep -Ev "grep|%s"|wc -l'%(processes_name,__file__))
[root@db1 ~]# chmod +x /etc/zabbix/scripts/detect_proc.py
```

#### 修改配置文件

然后我们修改zabbix agent的配置文件，添加一行内容。
这里我们定义了一个名为proc.item的key，这个key会包含chuan传参，在[]内，这个key调用的脚本事/root/detect_proc.py
```bash
# vim  /etc/zabbix/zabbix_agentd.conf
UserParameter=proc.item[*],/etc/zabbix/scripts/detect_proc.py $1
```
#### 重启服务

重启zabbix-agent服务
```bash
[root@db1 ~]# systemctl restart zabbix-agent
```

#### zabbix server端验证

这里我们通过三条命令多角度验证吗，首先是不传参，结果报错。然后我们传入/usr/sbin/sshd，结果打印1，表示有一条进程匹配，然后我们传入elastic，打印0，表示0条匹配。

```bash
[root@zabbix ~]# zabbix_get -s db1 -k proc.item
Traceback (most recent call last):
  File "/etc/zabbix/scripts/detect_proc.py", line 3, in <module>
    processes_name=sys.argv[1]
IndexError: list index out of range
[root@zabbix ~]# zabbix_get -s db1 -k proc.item[/usr/sbin/sshd]
1
[root@zabbix ~]# zabbix_get -s db1 -k proc.item[elastic]
0

```

#### zabbix web端添加监控
这里我们省略掉一些本文前面写到过的基本操作，直接到创建item那里。

<img src=../images/37.jpg>

等待30秒，然后在latest data里面，我们可以看到已经有数据了。

<img src=../images/38.jpg>


创建trigger告警

<img src=../images/39.jpg>

这里我停掉ssh服务试一下，我的是虚拟机，停掉ssh服务后xshell无法通过ssh连接了，这里我直接在虚拟机里关闭ssh服务

<img src=../images/40.jpg>

然后30秒内告警邮件就来了。

<img src=../images/41.jpg>

然后去启动服务，服务恢复的邮件就来了。

<img src=../images/42.jpg>