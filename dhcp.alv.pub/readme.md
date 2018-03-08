
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

- dhcp.alv.pub server function

Provide dhcp service, and guide next server for pxe installation.

- dhcp.alv.pub basic information
```
Hostname:dhcp.alv.pub
Description: dhcp server
NIC1 Type: NAT
NIC1 IP:192.168.127.1
NIC2 Type: VMnet1
NIC2 IP:192.168.38.1
Default Gateway:192.168.127.2
```

- [x] Provide update dhcp command at ansible.
```bash
ansible dhcp -m command -a 'sudo python -c "$(curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/dhcp.alv.pub/updateDhcpd.py)"'
```

- System Preinstallation
```bash
bash -c "$(curl -fsSL https://github.com/AlvinWanCN/scripts/raw/master/common_tools/disableSeAndFir.sh)" #自定义脚本的方式关闭防火墙
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/pullLocalYum.py)" #添加本地yum仓库
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/joinNatashaLDAP.py)" #加入到我的ldap
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/shell/pxe/set_hostname.py)" #根据ip修改主机名
```

- Scripts
```bash
# vim /root/bin/updateDhcpdfile.py #re pull dhcp configuration and restart dhcp service.
#!/usr/bin/python
#conding:utf-8
import os
url='https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/dhcp.alv.pub/dhcpd.conf'
file='/etc/dhcp/dhcpd.conf'
os.system('curl -fsSL %s > %s'%(url,file))
os.system('systemctl restart dhcpd')

```

- dhcp installation
```bash
# yum install dhcp -y
```

- dhcp configuration

```sybase
# curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/dhcp.alv.pub/dhcpd.conf > /etc/dhcp/dhcpd.conf
```
