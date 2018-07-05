
# Create Repository

## Make Openstack Repository


```
#下载OpenStack安装包(仅作为参考，根据需求添加其它组件)
yum install centos-release-openstack-pike -y #安装OpenStack官方源
sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
mkdir -p /www/share/centos7_openstack_rpm/
yum install --downloadonly --downloaddir=/www/share/centos7_openstack_rpm/ -y \
python-openstackclient openstack-selinux python-openstackclient python2-PyMySQL \
openstack-utils \
mariadb mariadb-server mariadb-galera-server python2-PyMySQL \
erlang socat rabbitmq-server \
openstack-keystone httpd mod_wsgi memcached python-memcached \
apr apr-util \
openstack-glance python-glance \
openstack-nova-api openstack-nova-conductor \
openstack-nova-console openstack-nova-novncproxy \
openstack-nova-scheduler openstack-nova-placement-api \
openstack-nova-compute python-openstackclient openstack-selinux \
openstack-neutron openstack-neutron-ml2 \
openstack-neutron-linuxbridge python-neutronclient ebtables ipset \
openstack-neutron-linuxbridge ebtables ipset \
openstack-dashboard \
openstack-cinder targetcli python-keystone lvm2 \
corosync pacemaker pcs fence-agents resource-agents \
openstack-neutron-linuxbridge

#更新源
yum install createrepo -y
createrepo --update -p /www/share/centos7_openstack_rpm/
```

## 添加到nginx里

在原有文件里添加如下内容。
```
# vim /etc/nginx/conf.d/pxe.conf
        location /openstack_pick_centos7 {
                alias   /www/share/centos7_openstack_rpm;
                autoindex on;
        }
```

## 使用该仓库

```
# vim /etc/yum.repos.d/openstack_pick_centos7.repo
[openstack_pick_centos7]
name=openstack_pick_centos7
baseurl=http://dc.alv.pub/openstack_pick_centos7
gpgcheck=0
enabled=1
```

## 在github里更新之后的一键添加操作。

```
curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo
```