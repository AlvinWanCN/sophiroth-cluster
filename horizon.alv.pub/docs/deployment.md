

# Deployments
该服务器上我们主要是用于两个用途，一是openstack客户端，二是Dashboard web管理界面，这里的Dashboard我使用horizone

##下面我们是先安装openstack客户端

### 更换阿里云

```
mkdir -p /etc/yum.repos.d/backup
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/backup/
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

yum install centos-release-openstack-pike -y #安装OpenStack库
mv /etc/yum.repos.d/CentOS-QEMU-EV.repo /tmp/
yum clean all && yum makecache #生成缓存

```


### 安装openstack客户端和相关工具

```
yum install python-openstackclient openstack-selinux python2-PyMySQL -y #OpenStack客户端
yum install openstack-utils -y #openstack工具
```


### 创建 OpenStack 客户端环境脚本

以下操作是在openstack客户端做的，这里我们是在horizon.alv.pub上做的, 做这些操作之前，是已经在keystone1.alv.pub 上安装好了keystone了。

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

#### 测试脚本是否生效

```
source ./admin-openstack.sh
openstack token issue
```

#### 创建service项目,创建glance,nova,neutron用户，并授权

```
openstack project create --domain default --description "Service Project" service
openstack user create --domain default --password=glance glance
openstack role add --project service --user glance admin
openstack user create --domain default --password=nova nova
openstack role add --project service --user nova admin
openstack user create --domain default --password=neutron neutron
openstack role add --project service --user neutron admin
```

#### 创建demo项目(普通用户密码及角色)

```
openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password=demo demo
openstack role create user
openstack role add --project demo --user demo user
```

#### demo环境脚本

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

#### 测试脚本是否生效
```
source ./demo-openstack.sh
openstack token issue
```


## 安装配置horizon

### 安装软件

```
yum install openstack-dashboard python-memcached -y
```

### 配置

```
cp /etc/openstack-dashboard/local_settings{,.bak}
#egrep -v '#|^$' /etc/openstack-dashboard/local_settings #显示默认配置
Setfiles=/etc/openstack-dashboard/local_settings
sed -i 's#_member_#user#g' $Setfiles
sed -i 's#OPENSTACK_HOST = "127.0.0.1"#OPENSTACK_HOST = "keystone1.alv.pub"#' $Setfiles
##允许所有主机访问#
sed -i "/ALLOWED_HOSTS/cALLOWED_HOSTS = ['*', ]" $Setfiles
#去掉memcached注释#
sed -in '153,158s/#//' $Setfiles
sed -in '160,164s/.*/#&/' $Setfiles
sed -i 's#UTC#Asia/Shanghai#g' $Setfiles
sed -i 's#%s:5000/v2.0#%s:5000/v3#' $Setfiles

sed -i '/ULTIDOMAIN_SUPPORT/cOPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True' $Setfiles
sed -i "s@^#OPENSTACK_KEYSTONE_DEFAULT@OPENSTACK_KEYSTONE_DEFAULT@" $Setfiles
```

```
echo '
#set
OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 2,
}
#'>>$Setfiles
#
```


```
systemctl enable httpd
systemctl restart httpd
```



