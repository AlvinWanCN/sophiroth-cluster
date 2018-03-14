<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

## Restart cluster

#### 集群下服务器全部down掉的情况下，按如下操作

找到vim /var/lib/mysql/grastate.dat 里面safe_to_bootstrap=1的那台服务器，先启动那台服务器上的mysql服务，service mysql start --wsrep-new-cluster  然后启动其他服务器上的。service mysql start。

第一个启动的服务器，启动的时候要加--wsrep-new-cluster


## 相关报错处理

#### 问题1

 failed to open gcomm backend connection: 131: invalid UUID:

#### 解决方案：  

 mv /var/lib/mysql/gvwstate.dat /var/lib/mysql/gvwstate.dat.bak