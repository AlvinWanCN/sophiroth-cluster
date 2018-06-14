


<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>
# Neutron compute node deployment
## Neutron computer node


## Installation
```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
yum install -y openstack-neutron openstack-neutron-ml2 \
openstack-neutron-linuxbridge python-neutronclient ebtables ipset
```

## Configuration

```
cp /etc/neutron/neutron.conf{,.bak}
```

```
echo '#
[DEFAULT]
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub

[keystone_authtoken]
auth_uri = http://controller.alv.pub:5000
auth_url = http://controller.alv.pub:35357
memcached_servers = controller.alv.pub:11211
auth_type = password
project_domain_id = default
user_domain_id = default
project_name = service
username = neutron
password = neutron

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
#'>/etc/neutron/neutron.conf
```

### 在nova计算节点添加配置
以下配置在controller.alv.pub上添加
```
echo '
#
[neutron]
url = http://controller.alv.pub:9696
auth_url = http://controller.alv.pub:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
#'>>/etc/nova/nova.conf

systemctl restart openstack-nova-api.service
```

继续在neutron-computer1.alv.pub上的操作

```
cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini{,bak}
```

#ens32是网卡名

```
echo '
[linux_bridge]
physical_interface_mappings = provider:ens32
[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
[vxlan]
enable_vxlan = false
# local_ip = 10.2.1.21
# l2_population = true
#'>/etc/neutron/plugins/ml2/linuxbridge_agent.ini

```

```
#重启相关服务
systemctl restart openstack-nova-compute.service
#启动neutron
systemctl enable neutron-linuxbridge-agent.service
systemctl start neutron-linuxbridge-agent.service
```

## openstack客户端查看


```
openstack network agent list
```

```
[root@horizon ~]# openstack network agent list
[root@controller ~]# openstack network agent list
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+
| ID                                   | Agent Type         | Host                      | Availability Zone | Alive | State | Binary                    |
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+
| 000092fa-717c-4d69-98f2-52619289c1e8 | Linux bridge agent | controller.alv.pub        | None              | :-)   | UP    | neutron-linuxbridge-agent |
| 32507b66-6ca8-45d5-8896-e788de059545 | Metadata agent     | controller.alv.pub        | None              | :-)   | UP    | neutron-metadata-agent    |
| ceb24b93-e0fc-44ed-9bd1-ac0ec98b958f | L3 agent           | controller.alv.pub        | nova              | :-)   | UP    | neutron-l3-agent          |
| cec418ec-dd71-4489-b19f-43d9f180c4c1 | Linux bridge agent | neutron-computer1.alv.pub | None              | :-)   | UP    | neutron-linuxbridge-agent |
| e963fc2e-90f9-476e-a891-77bfa847fc7e | DHCP agent         | controller.alv.pub        | nova              | :-)   | UP    | neutron-dhcp-agent        |
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+

```