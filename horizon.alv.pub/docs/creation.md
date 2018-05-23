# Openstack Creation

## 创建密钥

```
source ./admin-openstack.sh
echo ' 创建秘钥'
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
nova keypair-add --pub-key ~/.ssh/id_dsa.pub mykey
```

## 创建云主机类型

```
openstack flavor create --id 1 --vcpus 1 --ram 512 --disk 5  m1.nano
```


## 创建安全规则

```
openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 'default'

```

## 创建网络

### 本机网段
```
IP=`ip add|grep global|awk -F'[ /]+' '{ print $3 }'|head -n 1`
IPS=`echo $IP|awk -F\. '{ print $1"."$2"."$3 }'`
echo $IPS
```

### 创建网络
```
openstack network create --share --external --provider-physical-network provider --provider-network-type flat lan_$IPS
```

### 创建子网

```
openstack subnet create --network lan_$IPS --allocation-pool start=$IPS.130,end=$IPS.200  --dns-nameserver 47.75.0.56 --gateway $IPS.254 --subnet-range $IPS.0/24 net_$IPS
```


### 下载测试镜像

```
wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
```

### 上传镜像到镜像服务

```
openstack image create "cirros" --file cirros-0.3.5-x86_64-disk.img  --disk-format qcow2 --container-format bare --public

```

### 创建虚拟机 VM01

```
nova boot --flavor m1.nano --image cirros \
  --nic net-name=lan_$IPS --security-group default --key-name mykey \
  VM01
```

### 查看虚机列表

```
openstack server list
```