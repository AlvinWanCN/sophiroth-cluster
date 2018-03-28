<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>




<img src='http://img.blog.csdn.net/20170301165648805?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGhyb21l/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center'>

设置iptables允许包转发，设置postrouting。</br>
ens34是内网网卡，ens33是外网网卡。
```bash
# iptables -A FORWARD -i ens34 -j ACCEPT
# iptables -t nat -A POSTROUTING -s 192.168.38.0/24 -o ens33 -j MASQUERADE
```

打开Linux的转发功能，可以执行如下命令


```bash
# echo 1 > /proc/sys/net/ipv4/ip_forward
```


