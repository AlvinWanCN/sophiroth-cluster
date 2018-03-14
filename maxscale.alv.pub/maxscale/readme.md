<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>



## Reference material
 url: https://mariadb.com/kb/en/mariadb-enterprise/mariadb-maxscale-14/maxscale-readwrite-splitting-with-galera-cluster/
url:http://blog.csdn.net/lyk_for_dba/article/details/78351124
## Install maxscale
```bash
# yum install https://downloads.mariadb.com/MaxScale/2.1.9/rhel/7/x86_64/maxscale-2.1.9-1.rhel.7.x86_64.rpm
```

## Configuration file
```bash
[root@maxscale ~]# ls -l /etc/maxscale.cnf
-rw-r--r-- 1 root root 2079 Mar 12 17:12 /etc/maxscale.cnf

```

## make key
```bash
[root@maxscale ~]# maxkeys /var/lib/maxscale/ #在指定目录下生成加密密码规格
[root@maxscale ~]# maxpasswd /var/lib/maxscale/ sophiroth ##给sophiroth加密 生成加密后密码（此处和mysql赋权时密码一致，将生成的密码贴在配置文件中）
BBF537B460B777BCA9A656DF5702E33C
```



## Configure maxscale

```bash
# confFileUrl='https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/maxscale.alv.pub/maxscale/conf.d/maxscale.cnf'
# curl -fsSL $confFileUrl > /etc/maxscale.conf
##这里需要手动将前面生成的加密密码替换掉配置文件里面的那个密码，由于加密方式不一样，所以每次同样的密码的密文也会不一样。
# chown maxscale /var/lib/maxscale/ -R
# systemctl start maxscale
# systemctl enable maxscale
[root@maxscale ~]# maxscale --version
MaxScale 2.1.9

[root@maxscale ~]# maxadmin list servers
Servers.
-------------------+-----------------+-------+-------------+--------------------
Server             | Address         | Port  | Connections | Status              
-------------------+-----------------+-------+-------------+--------------------
server1            | 192.168.127.52  |  3306 |           0 | Slave, Synced, Running
server2            | 192.168.127.53  |  3306 |           0 | Master, Synced, Running
server3            | 192.168.127.57  |  3306 |           0 | Slave, Synced, Running
-------------------+-----------------+-------+-------------+--------------------
[root@maxscale ~]# maxadmin list monitors
---------------------+---------------------
Monitor              | Status
---------------------+---------------------
Galera Monitor       | Running
---------------------+---------------------
[root@maxscale ~]# maxadmin list services
Services.
--------------------------+-------------------+--------+----------------+-------------------
Service Name              | Router Module     | #Users | Total Sessions | Backend databases
--------------------------+-------------------+--------+----------------+-------------------
Read-Write Service        | readwritesplit    |      1 |              1 | server1, server2, server3
MaxAdmin Service          | cli               |      2 |              5 | 
--------------------------+-------------------+--------+----------------+-------------------

```
