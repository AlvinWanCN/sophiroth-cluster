<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>




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
# /etc/init.d/mysql start   #集群的第一个节点启动时需要加--wsrep-new-cluster 参数，其他节点接下来启动时不需要加。
```
