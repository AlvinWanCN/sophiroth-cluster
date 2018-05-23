


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
auth_uri = http://keystone1.alv.pub:5000
auth_url = http://keystone1.alv.pub:35357
memcached_servers = keystone1.alv.pub:11211
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
以下配置在nova-computer1.alv.pub上添加
```
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
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+
| ID                                   | Agent Type         | Host                      | Availability Zone | Alive | State | Binary                    |
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+
| 38dc3afd-bd09-4511-ae8f-043084c8aa63 | Linux bridge agent | neutron-computer1.alv.pub | None              | :-)   | UP    | neutron-linuxbridge-agent |
| 4a21284a-4eb7-4fec-97af-5e8fbfe2f4ac | Linux bridge agent | neutron.alv.pub           | None              | :-)   | UP    | neutron-linuxbridge-agent |
| c5f0b414-7f37-455f-8fb5-172a6e4cad82 | Metadata agent     | neutron.alv.pub           | None              | :-)   | UP    | neutron-metadata-agent    |
| df69adb5-5695-4230-929a-fd587846c1af | DHCP agent         | neutron.alv.pub           | nova              | :-)   | UP    | neutron-dhcp-agent        |
+--------------------------------------+--------------------+---------------------------+-------------------+-------+-------+---------------------------+
```