<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


```bash
$ vim vpn.env
VPN_IPSEC_PSK=xxxx
VPN_USER=xxxx
VPN_PASSWORD=xxxxxxx
$ sudo docker run     --name ipsec-vpn-server     --env-file ./vpn.env     --restart=always     -p 500:500/udp     -p 4500:4500/udp     -v /lib/modules:/lib/modules:ro     -d --privileged     hwdsl2/ipsec-vpn-server
```


