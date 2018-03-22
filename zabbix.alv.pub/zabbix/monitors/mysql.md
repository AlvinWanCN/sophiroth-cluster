<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


## zabbix 监控mysql

我们可以用zabbix自带的监控模块来监控mysql，但有些东西还需要配置，那就是用户名密码，在web端添加了监控之后，如果不设置客户端访问时的用户名密码，则会报错

这里我们通过修改/etc/my.cnf的方式来解决问题

```
# vim /etc/my.cnf
[client-server]
user=zabbix
password=zabbixpassword
```

设置好之后，我们验证一下,直接执行mysql，能登录到数据库，那很好

再执行一下 mysqladmin extended-status |grep -w "Bytes_received" |cut -d"|" -f3，有数据打印出来，那算ok了。



```
[root@natasha ~]# mysql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 14103
Server version: 5.5.57-MariaDB-wsrep MariaDB Server, wsrep_25.21.r9949137

Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> exit
Bye
[root@natasha ~]# mysqladmin extended-status |grep -w "Bytes_received" |cut -d"|" -f3
 56607472
 ```

然后我们zabbix web那里可以看到对mysql已经监控起来了。

<img src=../images/65.jpg>

在图表那里我们还可以看到mysql的各项操作的数据也都可以再一张图上看到。

<img src=../images/66.jpg>