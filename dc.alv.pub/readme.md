<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

### dc.alv.pub server function

provide ldap user home data directory;

provide yum repository contents.

### dc.alv.pub basic information

```
Hostname:dc.alv.pub
Description: data center server.
NIC1 Type: NAT
NIC1 IP:192.168.127.1
NIC2 Type: VMnet1
NIC2 IP:192.168.38.1
Default Gateway:192.168.127.2
```

### dc.alv.pub software installation
```bash
# yum install nginx
```

### dc.alv.pub nginx configuration and startup

```bash
# curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/dc.alv.pub/nginx/pxe.conf > /etc/nginx/conf.d/pxe.conf
# systemctl start nginx
# systemctl enable nginx
```


### 
