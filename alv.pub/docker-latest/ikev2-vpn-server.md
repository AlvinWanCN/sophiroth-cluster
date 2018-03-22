<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>




#### 启动一个ikev2 docker容器。

```
# docker run -d --name ikev2-vpn-server --privileged -p 500:500/udp -p 4500:4500/udp --restart=always  gaomd/ikev2-vpn-server:0.3.0
```

#### 创建连接vpn所需要的mobileconfig
```bash
# docker run -i -t --rm --volumes-from ikev2-vpn-server -e "HOST=alv.pub" gaomd/ikev2-vpn-server:0.3.0 generate-mobileconfig > ikev2-vpn.mobileconfig
```

#### 然后可以根据实际需求修改配置文件
比如修改连接名之类的。

```
# vim ikev2-vpn.mobileconfig
```

#### 将配置文件发给手机并安装

手机上需要安装那个配置文件用于创建VPN连接

这里我们可以通过邮件的方式来讲这个文件传到我们的手机上

```
# echo vpnkey|mail -s 'Alvin vpn key' -a ikev2-vpn.mobileconfig alvin.wan@xxxxxxx.xxx
```