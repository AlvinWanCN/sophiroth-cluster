<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


# nova computer node deployment



## Install nova

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
yum install -y openstack-nova-compute
yum install -y python-openstackclient openstack-selinux

```


## 设置Nova实例路径(磁盘镜像文件)

```
Vdir=/XLH_Data/nova
VHD=$Vdir/instances
mkdir -p $VHD
chown -R nova:nova $Vdir
```


## 使用QEMU或KVM ,KVM硬件加速需要硬件支持
```
[[ `egrep -c '(vmx|svm)' /proc/cpuinfo` = 0 ]] && { Kvm=qemu; } || { Kvm=kvm; }
echo "使用 $Kvm"
```

```
VncProxy=192.168.127.79 #VNC代理外网IP地址

```

## nova配置

```
/usr/bin/cp /etc/nova/nova.conf{,.$(date +%s).bak}
#egrep -v '^$|#' /etc/nova/nova.conf
echo '#
[DEFAULT]
instances_path='$VHD'
enabled_apis = osapi_compute,metadata
transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub
my_ip = 192.168.127.79
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver

[api_database]
connection = mysql+pymysql://nova:nova@maxscale.alv.pub:4006/nova_api
[database]
connection = mysql+pymysql://nova:nova@maxscale.alv.pub:4006/nova

[api]
auth_strategy = keystone
[keystone_authtoken]
auth_uri = http://keystone1.alv.pub:5000
auth_url = http://keystone1.alv.pub:35357
memcached_servers = keystone1.alv.pub:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = nova

[vnc]
enabled = true
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://'$VncProxy':6080/vnc_auto.html
[glance]
api_servers = http://glance.alv.pub:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://keystone1.alv.pub:35357/v3
username = placement
password = placement

[libvirt]
virt_type = '$Kvm'
#'>/etc/nova/nova.conf
#sed -i 's#nova1.alv.pub:6080#192.168.127.79:6080#' /etc/nova/nova.conf
```