<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


## salt 的分组

<img src=../images/1.png>


使用saltstack的原因是为了对批量的机器执行相同的操作。大的来说上千台机器，不可能所有的机器都运行相同的业务，有可能这一百台运行的是web、另外一百台运行的是db ，所以分组就显的比较有用。

首先如果不分组，直接用salt命令执行是不是也可以呢？

### 一、配置分组

```bash
[root@localhost ~]# salt -C 'P@os:CentOS' test.ping
host172:
    True
host174:
    True
```

 从上面执行的结果看，是OK的。那为什么还要引入分组，当然是为了简化这个过程，以后只需要 -N +组句就ok了，而且也便于区分。


为minion进行预先分组配置非常简单，只需要编辑/etc/salt/master文件即可。示例如下：

[root@localhost ~]# vim /etc/salt/master
nodegroups:
  group1: 'L@host172,host174'
  group2: 'S@192.168.10.172'
  group3: 'P@os:CentOS'
进行test.ping测试如下：

```
[root@localhost ~]# salt -N group1 test.ping
host172:
    True
host174:
    True
[root@localhost ~]# salt -N group2 test.ping
host172:
    True
[root@localhost ~]# salt -N group3 test.ping
host172:
    True
host174:
    True
```

### 二、分组语法

nodegroup分组时可以用到的语法关键字有G、E、P、L、I、S、R、D几个，几者的意义和用法如文档最上面的表所显示：


此外，匹配中可以使用and、or及not等boolean型操作。例：
```
[root@saltstack ~]# salt -C 'db1.alv.pub or db2.alv.pub' test.ping
db2.alv.pub:
    True
db1.alv.pub:
```

想匹配所有minion中主机名(minion id)以webserv开头并且运行在Debian系统上或者minion的主机名(minion id)匹配正则表达式web-dc1-srv.* ，就可以用下表方式表示：

salt -C 'webserv* and G@os:Debian or E@web-dc1-srv.*' test.ping

当然也可以在预先分组时将这个配置写在分组规则里。在top.sls中可以如下使用:

base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    – match: compound
    – webserver
参考页面：

http://docs.saltstack.com/topics/targeting/nodegroups.html

http://docs.saltstack.com/ref/states/top.html

```