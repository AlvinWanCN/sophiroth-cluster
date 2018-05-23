

# Neutron Deployment

#本实例网络配置方式是：公共网络

#官方参考 https://docs.openstack.org/neutron/pike/install/controller-install-rdo.html

## 创建Neutron数据库、用户认证，前面已设置

### 在数据库里的配置
这里我们是在maxscale.alv.pub里做以下操作
```
create database neutron;
grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'neutron';
grant all privileges on neutron.* to 'neutron'@'%' identified by 'neutron';
```


## 创建Neutron服务实体,API端点
这里我们在openstack客户端做以下配置，这里我们在horizon.alv.pub配置这些。

```
openstack service create --name neutron --description "OpenStack Networking" network
openstack endpoint create --region RegionOne network public http://neutron.alv.pub:9696
openstack endpoint create --region RegionOne network internal http://neutron.alv.pub:9696
openstack endpoint create --region RegionOne network admin http://neutron.alv.pub:9696
```

## 安装软件

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
yum install -y openstack-neutron openstack-neutron-ml2 \
openstack-neutron-linuxbridge python-neutronclient ebtables ipset
```

## Neutron 备份配置
```
cp /etc/neutron/neutron.conf{,.bak2}
cp /etc/neutron/plugins/ml2/ml2_conf.ini{,.bak}
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini{,.bak}
cp /etc/neutron/dhcp_agent.ini{,.bak}
cp /etc/neutron/metadata_agent.ini{,.bak}
cp /etc/neutron/l3_agent.ini{,.bak}
```

## 配置
```
echo '
[DEFAULT]
nova_metadata_ip = nova1.alv.pub
metadata_proxy_shared_secret = metadata
#'>/etc/neutron/metadata_agent.ini
#
echo '
#
[neutron]
url = http://neutron.alv.pub:9696
auth_url = http://keystone1.alv.pub:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = true
metadata_proxy_shared_secret = metadata
#'>>/etc/nova/nova.conf
#
echo '#
[ml2]
tenant_network_types =
type_drivers = vlan,flat
mechanism_drivers = linuxbridge
extension_drivers = port_security
[ml2_type_flat]
flat_networks = provider
[securitygroup]
enable_ipset = True
#vlan
# [ml2_type_valn]
# network_vlan_ranges = provider:3001:4000
#'>/etc/neutron/plugins/ml2/ml2_conf.ini
# bond0是网卡名
echo '#
[linux_bridge]
physical_interface_mappings = provider:ens32
[vxlan]
enable_vxlan = false
#local_ip = 10.2.1.20
#l2_population = true
[agent]
prevent_arp_spoofing = True
[securitygroup]
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
enable_security_group = True
#'>/etc/neutron/plugins/ml2/linuxbridge_agent.ini
#
echo '#
[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
#'>/etc/neutron/dhcp_agent.ini
#
echo '
[DEFAULT]
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub
auth_strategy = keystone
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true

[keystone_authtoken]
auth_uri = http://keystone1.alv.pub:5000
auth_url = http://keystone1.alv.pub:35357
memcached_servers = keystone1.alv.pub:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = neutron

[nova]
auth_url = http://keystone1.alv.pub:35357
auth_type = password
project_domain_id = default
user_domain_id = default
region_name = RegionOne
project_name = service
username = nova
password = nova

[database]
connection = mysql://neutron:neutron@maxscale.alv.pub:4006/neutron

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
#'>/etc/neutron/neutron.conf
#
echo '
[DEFAULT]
interface_driver = linuxbridge
#'>/etc/neutron/l3_agent.ini
```

## 同步数据库
```
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```
## 检测数据


```
mysql -h maxscale.alv.pub -P4006 -u neutron -pneutron -e "use neutron;show tables;"

```

## 重启相关服务
在nova1.alv.pub上执行

```
systemctl restart openstack-nova-api.service

```

## 启动neutron
```
systemctl enable neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
systemctl start neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
echo "查看网络,正常是：控制节点3个ID"

```

openstack 客户端执行
```
openstack network agent list
```


# Deploy Neutron Compute node

## Install Software

```

```