
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

## zabbix service

reference url:http://blog.csdn.net/u014057054/article/details/66476990
## system post installation
- [x] 系统完成安装时自动已执行的脚本
bash -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/pxe_system/scripts/post_installation.sh)"
## Zabbix Installation

### add zabbix 3.4 yum reposiroty
```bash
# curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/zabbix3.4.repo > /etc/yum.repos.d/zabbix3.4.repo
```
### add epel yum repository
```bash
# curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/Centos7-extras.repo > /etc//yum.repos.d/Centos7-extras.repo
# yum install epel-release -y
```
### Install zabbix packages

```bash
# yum install zabbix-* -y #this installation will include httpd and php and some depended packages.
```
### Configure database
这里我们使用的不是本地的数据库，而是一个已经配置好的数据库集群，我们通过数据库的前端maxscale访问数据。</br>
先在数据库离配置好zabbix需要用的数据库和用户名密码和权限。
```sql
MySQL [(none)]> create database zabbix default character set utf8 collate utf8_bin;
Query OK, 1 row affected (0.01 sec)
MariaDB [(none)]> grant all privileges on zabbix.* to 'zabbix'@'%' identified by 'zabbix';
Query OK, 0 rows affected (0.01 sec)

```

### import zabbix database structure
需要mysql客户端，所以我们先安装一个mysql,然后进去相关目录开始导入数据到我们指定的数据库。
```bash
[root@zabbix ~]# yum install mysql -y
[root@zabbix ~]# cd /usr/share/doc/zabbix-server-mysql-3.4.7/
[root@zabbix zabbix-server-mysql-3.4.7]# zcat create.sql.gz|mysql -uzabbix -pzabbix -P4006 -hmaxscale zabbix
```

### Configure zabbix server
这里我们主要要注意数据库的配置是否正确
```bash
# curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/zabbix.alv.pub/zabbix/conf.d/zabbix_server.conf > /etc/zabbix/zabbix_server.conf 
[root@zabbix ~]# vim /etc/zabbix/zabbix_server.conf 
[root@zabbix ~]# 
[root@zabbix ~]# egrep -v "^$|^#" /etc/zabbix/zabbix_server.conf 
LogFile=/var/log/zabbix/zabbix_server.log
LogFileSize=0
PidFile=/var/run/zabbix/zabbix_server.pid
SocketDir=/var/run/zabbix
DBHost=maxscale
DBName=zabbix
DBUser=zabbix
DBPassword=zabbix
DBPort=4006
SNMPTrapperFile=/var/log/snmptrap/snmptrap.log
Timeout=4
AlertScriptsPath=/usr/lib/zabbix/alertscripts
ExternalScripts=/usr/lib/zabbix/externalscripts
LogSlowQueries=3000

```

### Configure httpd service
修改zabbix时区，在19行，将注销去掉，将时区改为本地时区，这里我们改成亚洲上海。
```bash
[root@zabbix ~]# vim /etc/httpd/conf.d/zabbix.conf 
        php_value date.timezone Asia/Shanghai
```

### start and enable zabbix-server and httpd

```bash
[root@zabbix ~]# systemctl start zabbix-server httpd
[root@zabbix ~]# systemctl enable zabbix-server httpd
Created symlink from /etc/systemd/system/multi-user.target.wants/zabbix-server.service to /usr/lib/systemd/system/zabbix-server.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.

```

### visit zabbix web 
visit url : http://zabbix.alv.pub/zabbix

and setup zabbix server.

web前端简单的配置结束之后，输入用户名面登录，默认用户名是Admin，密码是zabbix。


### zabbix agent installation
在配置好了zabbix的yum 仓库后，直接一条命令yum安装就好了。
添加zabbix3.4 yum仓库的命令如下，已经添加了的服务器就不用再次执行了。
```bash
# curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/zabbix3.4.repo > /etc/yum.repos.d/zabbix3.4.repo
```
安装zabbix-agent
```bash
yum install zabbix-agent -y
```

### Configure zabbix-agent.

