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

