<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


## dns service

这里我们使用的软件是bind, 安装后的服务是named，提供dns服务。

这里要注意的是，如果我们的dns服务器是能通过外网直接访问到的，而我们的目的不是对外公共提供服务的，那我们需要设置好防火墙规则。

dns服务是使用的udp协议53号端口，一个客户端就可以通过该端口占用dns服务器不小的流量。

所以我们需要让udp 53号端口只提供给我们允许的IP访问。