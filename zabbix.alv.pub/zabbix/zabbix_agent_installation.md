<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>




### zabbix alv.pub zone auto installation and configuration script

```bash
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/zabbix.alv.pub/zabbix/scripts/installZabbixAgent.py)"
```


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

### Configuration zabbix-agent.

```bash
# sed -i "s/^Hostname.*/Hostname=$(hostname)/" /etc/zabbix/zabbix_agentd.conf
# sed -i "s/^Server.*/Server=zabbix.alv.pub/" /etc/zabbix/zabbix_agentd.conf
```

### Start up zabbix-agent

```bash
# systemctl start zabbix-agent
# systemctl enable zabbix-agent
```