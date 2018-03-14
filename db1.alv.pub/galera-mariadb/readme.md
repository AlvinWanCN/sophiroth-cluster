<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


## cluster server information

<html>
<table>
    <thead>
        <th>Role</th>
        <th>Hostname</th>
        <th>IP</th>
        <th>OS</th>
        <th>User</th>
        <th>Selinux</th>
        <th>Firewalld</th>
    </thead>
    <tr>
        <td>Server</td>
        <td>db1.alv.pub</td>
        <td>192.168.127.52</td>
        <td>centos7.4</td>
        <td>root</td>
        <td>disabled</td>
        <td>disabled</td>
    </tr>
    <tr>
        <td>Server</td>
        <td>db2.alv.pub</td>
        <td>192.168.127.53</td>
        <td>centos7.4</td>
        <td>root</td>
        <td>disabled</td>
        <td>disabled</td>
    </tr>
    <tr>
        <td>Server</td>
        <td>db3.alv.pub</td>
        <td>192.168.127.57</td>
        <td>centos7.4</td>
        <td>root</td>
        <td>disabled</td>
        <td>disabled</td>
    </tr>
</table>
 </html>



## mariadb galera cluster installation

- Configure yum repository 
```bash
# vim /etc/yum.repos.d/galera.repo 
[galera]
name=galera
baseurl=http://mirrors.tuna.tsinghua.edu.cn/mariadb/mariadb-5.5.57/yum/centos7-amd64/
gpgcheck=0
```

- Install  MariaDB-Galera-server 
```bash
# yum install MariaDB-Galera-server -y
```

- Configure mariadb
```bash
# vim /etc/my.cnf.d/server.cnf
[mysqld]
character_set_server=utf8
lower_case_table_names=1

[galera]
wsrep_provider=/usr/lib64/galera/libgalera_smm.so
wsrep_cluster_address="gcomm://192.168.127.52,192.168.127.53,192.168.127.57"
binlog_format=row
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0
wsrep_cluster_name="galera_cluster"
```

- Start up
```bash
# /etc/init.d/mysql start --wsrep-new-cluster   #集群的第一个节点启动时需要加--wsrep-new-cluster 参数，其他节点接下来启动时不需要加。
```

- 进入数据库
```sql
# mysql
```

- 创建sophiroth数据库

```sql
MariaDB [(none)]> create database sophiroth default charset='utf8';
Query OK, 1 row affected (0.01 sec)

```
- 创建一个账号，授权该账号拥有sophiroth数据库的所有权限。
```sql
MariaDB [(none)]> grant all privileges on sophiroth.* to 'alvin'@'%' identified by 'sophiroth';
Query OK, 0 rows affected (0.01 sec)

```

- 用刚才创建的账号访问其他集群内的服务。

```bash
[root@db1 ~]# mysql -ualvin -psophiroth -h db2 -e "show databases;"
+--------------------+
| Database           |
+--------------------+
| information_schema |
| sophiroth          |
| test               |
+--------------------+
[root@db1 ~]# 
[root@db1 ~]# mysql -ualvin -psophiroth -h db3 -e "show databases;"
+--------------------+
| Database           |
+--------------------+
| information_schema |
| sophiroth          |
| test               |
+--------------------+

```

- 创建用于授权给maxscale使用的账号。



