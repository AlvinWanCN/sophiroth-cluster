## nat for aliyun intranet


第一条iptables命令表示接受来自eth0网段在我们这进行装发

第二条iptables命令表示POSTROUTING，POSTROUTING是源地址转换，要把你的内网地址转换成公网地址才能让你上网。


```bash
[root@natasha ~]# ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.31.33.93  netmask 255.255.240.0  broadcast 172.31.47.255
        ether 00:16:3e:02:13:8b  txqueuelen 1000  (Ethernet)
        RX packets 5293956  bytes 614041345 (585.5 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 753012  bytes 668844131 (637.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@natasha ~]#
[root@natasha ~]# iptables -A FORWARD -i eth0 -j ACCEPT
[root@natasha ~]# iptables -t nat -A POSTROUTING -s 172.31.0.0/16 -o eth0 -j MASQUERADE

```