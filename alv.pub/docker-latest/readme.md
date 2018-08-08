<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


### docker-latest
- Install docker-latest
```bash
# yum install docker-latest
```
- Start up docker-latest and enable.
```bash
# systemctl start docker-latest
# systemctl enable docker-latest
```
### l2tp/ipsec vpn
- setup a l2tp docker container
```bash
# modprobe af_key
# vim vpn.env
VPN_IPSEC_PSK=your_ipsec_pre_shared_key
VPN_USER=your_vpn_username
VPN_PASSWORD=your_vpn_password
# docker run \
    --name ipsec-vpn-server \
    --env-file ./vpn.env \
    --restart=always \
    -p 500:500/udp \
    -p 4500:4500/udp \
    -v /lib/modules:/lib/modules:ro \
    -d --privileged \
    hwdsl2/ipsec-vpn-server
```
If your server have firewall setting, you should open udp port 500 and 4500 at firewall.
### pptp vpn

<a href=https://github.com/AlvinWanCN/TechnologyCenter/blob/master/linux/docs/vpn/centos7_pptp_installation.md>Click here to view pptp service configuration</a>

### mariadb


### jenkins

```bash

# mkdir -p /jenkins
# chmod 777 /jenkins
# docker run -d -it --name jenkins -p 8001:8080 -p 50000:50000 -v /jenkins/:/var/jenkins_home -v /etc/localtime:/etc/localtime --restart on-failure jenkins
```
administrator password:15037ecf04a54683813acb68a409e551 </br>

