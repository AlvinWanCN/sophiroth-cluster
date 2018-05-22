
# keystone deployment

## 数据库里创建数据库并授权
这里我们进入到数据库里执行下面的操作。

```
create database keystone;
grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'keystone';
grant all privileges on keystone.* to 'keystone'@'%' identified by 'keystone';
flush privileges;
```
## 更换阿里源

```
mv /etc/yum.repos.d/CentOS-Base.repo{,.bak}
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
yum clean all && yum makecache #生成缓存
```

## Software Installation
### Install Keystone

```
yum install -y openstack-keystone httpd mod_wsgi memcached python-memcached
yum install apr apr-util -y
```

## memcached启动和设置

```
cp /etc/sysconfig/memcached{,.bak}
systemctl enable memcached.service
systemctl start memcached.service
netstat -antp|grep 11211
```

## Keystone 配置

```bash
cp /etc/keystone/keystone.conf{,.bak}  #备份默认配置
Keys=$(openssl rand -hex 10)  #生成随机密码
echo $Keys
echo "kestone  $Keys">>~/openstack.log
echo "
[DEFAULT]
admin_token = $Keys
verbose = true
[database]
connection = mysql+pymysql://keystone:keystone@maxscale.alv.pub:4006/keystone
[token]
provider = fernet
driver = memcache
[memcache]
servers = keystone1.alv.pub:11211
">/etc/keystone/keystone.conf

```

## 初始化身份认证服务的数据库
```
su -s /bin/sh -c "keystone-manage db_sync" keystone
```

### 检查表是否创建成功
```
mysql -ukeystone -pkeystone -hmaxscale.alv.pub -P4006 -e "use keystone;show tables;"
```

## 初始化密钥存储库

```
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```

## 设置admin用户（管理用户）和密码

```
keystone-manage bootstrap --bootstrap-password admin \
  --bootstrap-admin-url http://keystone1.alv.pub:35357/v3/ \
  --bootstrap-internal-url http://keystone1.alv.pub:5000/v3/ \
  --bootstrap-public-url http://keystone1.alv.pub:5000/v3/ \
  --bootstrap-region-id RegionOne
```

## apache配置

```
cp /etc/httpd/conf/httpd.conf{,.bak}
echo "ServerName keystone1.alv.pub">>/etc/httpd/conf/httpd.conf
ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

#Apache HTTP 启动并设置开机自启动
systemctl enable httpd.service
systemctl restart httpd.service
netstat -antp|egrep ':5000|:35357|:80'

```

## 创建 OpenStack 客户端环境脚本

以下操作是在openstack客户端做的，这里我们是在horizon.alv.pub上做的。

```
echo "
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://keystone1.alv.pub:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./admin-openstack.sh
```

### 测试脚本是否生效

```
source ./admin-openstack.sh
openstack token issue
```

### 创建service项目,创建glance,nova,neutron用户，并授权

```
openstack project create --domain default --description "Service Project" service
openstack user create --domain default --password=glance glance
openstack role add --project service --user glance admin
openstack user create --domain default --password=nova nova
openstack role add --project service --user nova admin
openstack user create --domain default --password=neutron neutron
openstack role add --project service --user neutron admin
```

### 创建demo项目(普通用户密码及角色)

```
openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password=demo demo
openstack role create user
openstack role add --project demo --user demo user
```

### demo环境脚本

```
echo "
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=demo
export OS_USERNAME=demo
export OS_PASSWORD=demo
export OS_AUTH_URL=http://keystone1.alv.pub:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./demo-openstack.sh
```

### 测试脚本是否生效
```
source ./demo-openstack.sh
openstack token issue
```