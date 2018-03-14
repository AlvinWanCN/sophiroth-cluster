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
# confFileUrl='https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/maxscale.alv.pub/maxscale/conf.d/maxscale.conf'
# curl -fsSL $confFileUrl > /etc/maxscale.conf
# 
```
