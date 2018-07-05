ceph1.alv.pub
######################

.. contents::

创建ceph账号

useradd -d /home/ceph -m ceph
echo sophiroth|passwd --stdin ceph
echo "ceph ALL = (root) NOPASSWD:ALL" >> /etc/sudoers.d/ceph
chmod 0440 /etc/sudoers.d/ceph
su - ceph
ssh-keygen -P '' -f ~/.ssh/id_dsa



//把公钥拷贝到各 Ceph 节点上

ssh-copy-id ceph@ceph1
ssh-copy-id ceph@ceph2
ssh-copy-id ceph@ceph3

在管理节点ceph1 上修改~/.ssh/config文件(若没有则创建)增加一下内容：

Host    ceph1

Hostname  ceph1.alv.pub

User              ceph

Host    ceph2

Hostname  ceph2.alv.pub

User              ceph

Host    ceph3

Hostname  ceph3.alv.pub

User              ceph

在各节点上安装ntp（防止时钟偏移导致故障）、openssh



#sudo yum install ntp ntpdate ntp-doc

#sudo yum install openssh-server

添加ceph的yum 仓库


curl -s https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/ceph.repo > /etc/yum.repos.d/ceph.repo



在管理节点nod1上进行安装准备(使用ceph用户）

//新建文件夹ceph-cluster

$cd ~

$mkdir ceph-cluster

$cd ceph-cluster



//安装ceph-deploy

# sudo yum install ceph-deploy



//若安装ceph后遇到麻烦可以使用以下命令进行清除包和配置

#ceph-deploy purge ceph1 ceph2 ceph3

#ceph-deploy purgedata ceph1 ceph2 ceph3

#ceph-deploy forgetkeys



安装ceph创建集群



//进入到创建ceph-cluster文件夹下，执行命令

#ceph-deploy new ceph1 ceph2 ceph3



//在生成的ceph.conf中加入（写入[global] 段下）

osd pool default size = 2



//如果你有多个网卡，可以把 public network 写入 Ceph 配置文件的 [global] 段下

#public network = {ip-address}/{netmask}



//安装ceph

#ceph-deploy install ceph1 ceph2 ceph3



//配置初始 monitor(s)、并收集所有密钥

# ceph-deploy mon create-initial


新建osd



//添加两个 OSD ，登录到 Ceph 节点、并给 OSD 守护进程创建一个目录。

#ssh ceph2

#sudo mkdir /var/local/osd0
sudo chown ceph /var/local/osd0

#exit



#ssh ceph3

#sudo mkdir /var/local/osd1
sudo chown ceph /var/local/osd1

#exit



//然后，从管理节点执行 ceph-deploy 来准备 OSD

#ceph-deploy osd prepare ceph2:/var/local/osd0 ceph3:/var/local/osd1



//最后，激活 OSD

#ceph-deploy osd activate ceph2:/var/local/osd0 ceph3:/var/local/osd1



//确保你对 ceph.client.admin.keyring 有正确的操作权限。

    #chmod +r /etc/ceph/ceph.client.admin.keyring



//检查集群的健康状况

#ceph health    #等 peering 完成后，集群应该达到 active + clean 状态。


2  在客服端上使用ceph存储空间：

准备client-node
通过admin-node节点执行命令：
ceph-deploy  install  client-node
注：本次实验client节点和管理节点都在一台服务器上，所以前面已经安装了ceph，
ceph-deploy admin   client-node  ---推送配置和keying到客户端

创建块设备
    sudo  rbd create foo --size 10000   --块设备大小
将ceph提供的块设备映射到client-node
    sudo rbd map foo --pool rbd

格式化设备
sudo mkfs.xfs  /dev/rbd0
挂载
sudo mount  /dev/rbd0 /mnt/cephdir/
常用命令：
rbd ls  //查看本机的rbd设备
rbd info foo  //查看模块rbd设备的相关信息
rbd showmapped  //查看rbd设备映射信息
ceph health  //ceph健康状态
ceph status  //ceph当前全部状态
ceph -w //实时监控ceph状态及变化
ceph osd dump //所有osd详细状态
ceph osd tree  //osd所在位置，及状态
ceph quorum_status //mon优先级状态
ceph mon dump  //mon节点状态
ceph mds dump  //mds详细状态
ceph --admin-daemon /var/run/ceph/ceph-osd.0.asok config show  //在osd上查看详细的配置信息
