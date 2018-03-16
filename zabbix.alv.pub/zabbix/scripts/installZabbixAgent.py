#!/usr/bin/python
import os

os.system('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/zabbix3.4.repo > /etc/yum.repos.d/zabbix3.4.repo')
os.system('yum install zabbix-agent -y')
os.system('sed -i "s/^Hostname=.*/Hostname=$(hostname)/" /etc/zabbix/zabbix_agentd.conf')
os.system('sed -i "s/^Server=.*/Server=zabbix.alv.pub/" /etc/zabbix/zabbix_agentd.conf')
os.system('sed -i "s/^ServerActive=.*/ServerActive=zabbix.alv.pub/" /etc/zabbix/zabbix_agentd.conf')
os.system('systemctl start zabbix-agent')
os.system('systemctl enable zabbix-agent')