<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

#pxe + Kickstart 无人值守安装系统

sophiroth cluster 中pxe系统的tftp服务部署在dc.alv.pub上。

- 安装软件
yum -y install tftp-server dhcp syslinux xinetd system-config-kickstart
cp /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example /etc/dhcp/dhcpd.conf



参考：https://www.linuxidc.com/Linux/2017-06/144789.htm


系统内存要在2G以上，否则安装系统时容易报错。


## update default 
after file default has been modify,update file default in sophiroth environment, execute the following command at dc.alv.pub
```bash
# curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/pxe_system/default > /var/lib/tftpboot/pxelinux.cfg/default
```