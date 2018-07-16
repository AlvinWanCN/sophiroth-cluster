openstack combine ceph
##########################

.. contents::



#openstack pike与ceph集成
###########################
#openstack节点

#openstack节点配置ceph源
#使用阿里源 #rm -f /etc/yum.repos.d/*.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
sed -i '/aliyuncs.com/d' /etc/yum.repos.d/*.repo #删除阿里内网地址
wget -O /etc/yum.repos.d/ceph-luminous-aliyun.repo  http://elven.vip/ks/yum/ceph-luminous-aliyun.repo
yum clean all && yum makecache #生成缓存
#ceph客户端安装
yum -y install ceph-common


###########################
#ceph管理节点

#创建POOL
ceph osd pool create volumes 128
ceph osd pool create images 128
ceph osd pool create vms 128

#ssh免密验证
curl http://elven.vip/ks/sh/sshkey.me.sh >sshkey.me.sh
#认证用户及密码#
echo "
USER=root
PASS=123321
">my.sh.conf
#hosts设置
echo "
#openstack
192.168.58.17   controller
192.168.58.16   compute01
192.168.58.14   storage1
">>/etc/hosts
#ssh批量认证#
sh ./sshkey.me.sh controller compute01 storage1

#推送ceph配置到client
cd /etc/ceph/
ceph-deploy config push controller compute01 storage1

###########################

#创建ceph用户和密钥
ceph auth get-or-create client.cinder mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rwx pool=vms, allow rx pool=images'
ceph auth get-or-create client.glance mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=images'
ceph auth get-or-create client.cinder-backup mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=backups'

#查询用户，写入文件
ceph auth get-or-create client.cinder >/etc/ceph/ceph.client.cinder.keyring
ceph auth get-or-create client.glance >/etc/ceph/ceph.client.glance.keyring
# scp /etc/ceph/ceph.client.cinder.keyring $Node:/etc/ceph/
# scp /etc/ceph/ceph.client.glance.keyring $Node:/etc/ceph/

###########################
#拷贝秘钥到对应节点,修改权限
#(nova,cinder都使用client.cinder)

#glance
Node=glance1.alv.pub
scp /etc/ceph/ceph.client.glance.keyring $Node:/etc/ceph/
ssh $Node sudo chown glance:glance /etc/ceph/ceph.client.glance.keyring

#nova compute
Node=nova1.alv.pub
scp /etc/ceph/ceph.client.cinder.keyring $Node:/etc/ceph/
ssh $Node sudo chown nova:nova /etc/ceph/ceph.client.cinder.keyring
scp /etc/ceph/ceph.client.glance.keyring $Node:/etc/ceph/
ssh $Node sudo chown nova:nova /etc/ceph/ceph.client.glance.keyring

#cinder storage
Node=cinder1.alv.pub
scp /etc/ceph/ceph.client.cinder.keyring $Node:/etc/ceph/
ssh $Node sudo chown cinder:cinder /etc/ceph/ceph.client.cinder.keyring

###########################
#openstack glance配置

ls -l /etc/ceph/

#更改glance默认存储为ceph
cp -f /etc/glance/glance-api.conf{,bak2}
sed -i 's/^stores/#&/' /etc/glance/glance-api.conf
sed -i 's/^default_store/#&/' /etc/glance/glance-api.conf
echo '#[glance_store]
stores = rbd,file
default_store = rbd
rbd_store_pool = images
rbd_store_user = glance
rbd_store_ceph_conf = /etc/ceph/ceph.conf
rbd_store_chunk_size = 8
'>>/etc/glance/glance-api.conf

#重启服务
systemctl restart openstack-glance-api openstack-glance-registry

###########################
#nova计算节点

ls -l /etc/ceph/
#ceph
echo '
[client]
rbd cache = true
rbd cache writethrough until flush = true
admin socket = /var/run/ceph/guests/$cluster-$type.$id.$pid.$cctid.asok
log file = /var/log/qemu/qemu-guest-$pid.log
rbd concurrent management ops = 20

[client.cinder]
keyring = /etc/ceph/ceph.client.cinder.keyring
'>>/etc/ceph/ceph.conf

mkdir -p /var/run/ceph/guests/ /var/log/qemu/
chown qemu:libvirt /var/run/ceph/guests /var/log/qemu/

#密钥加进libvirt
#MyUID=$(uuidgen) && echo $MyUID #生成UID后面会用到#
MyUID=5d8bc172-d375-4631-8be0-cbe11bf88a55
Key=$(awk '/key/ { print $3 }' /etc/ceph/ceph.client.cinder.keyring)
echo '
<secret ephemeral="no" private="no">
<uuid>'$MyUID'</uuid>
<usage type="ceph">
<name>client.cinder secret</name>
</usage>
</secret>
'>ceph.xml
virsh secret-define --file ceph.xml
virsh secret-set-value --secret $MyUID  --base64 $Key

#nova配置
#注释原[libvirt]部分
sed -i 's/\[libvirt\]/#&/'  /etc/nova/nova.conf
sed -i 's/^virt_type/#&/'  /etc/nova/nova.conf
#使用ceph存储
echo '
[libvirt]
virt_type = qemu

images_type = rbd
images_rbd_pool = vms
images_rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_user = cinder
rbd_secret_uuid = '$MyUID'
disk_cachemodes="network=writeback"
live_migration_flag="VIR_MIGRATE_UNDEFINE_SOURCE,VIR_MIGRATE_PEER2PEER,VIR_MIGRATE_LIVE,VIR_MIGRATE_PERSIST_DEST,VIR_MIGRATE_TUNNELLED"
#禁用文件注入#
libvirt_inject_password = false
libvirt_inject_key = false
libvirt_inject_partition = -2
'>>/etc/nova/nova.conf

#重启服务
systemctl restart libvirtd.service openstack-nova-compute.service

###########################
#Cinder storage 添加Ceph存储

#enabled_backends添加ceph
sed -i 's/^enabled_backends.*/&,ceph/' /etc/cinder/cinder.conf
echo '
[ceph]
volume_driver = cinder.volume.drivers.rbd.RBDDriver
rbd_pool = volumes
rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_flatten_volume_from_snapshot = false
rbd_max_clone_depth = 5
rbd_store_chunk_size = 4
rados_connect_timeout = -1
glance_api_version = 2
rbd_user = cinder
rbd_secret_uuid = 5d8bc172-d375-4631-8be0-cbe11bf88a55
'>>/etc/cinder/cinder.conf

#重启服务
systemctl restart openstack-cinder-volume.service

###########################



###########################
#检测

#在openstack管理节点
source admin-openstack.sh

#查看cinder是否有@ceph存储
cinder service-list

#使用raw磁盘格式,创建镜像
source ./admin-openstack.sh
openstack image create "cirros2" \
  --file cirros-0.3.5-x86_64-disk.img \
  --disk-format raw --container-format bare \
  --public

#检查是否上传成功
openstack image list

#创建VM (cpu16是可用域)
NET=de98a7e6-6aaf-4569-b0bf-971cfb4ffbc8
nova boot --flavor m1.nano --image cirros2 \
  --nic net-id=$NET \
  --security-group default --key-name mykey \
  --availability-zone cpu16 \
  kvm04

#检查
openstack server list

#虚拟控制台访问实例
openstack console url show kvm04

#创建云盘volume
openstack volume create --size 1 disk01
#openstack volume list
#给虚机kvm04添加云盘
openstack server add volume kvm04 disk01

###########################
#在ceph管理节点查看
ceph df
#查看pool
rbd -p vms ls
rbd -p volumes ls
rbd -p images ls

###########################
#参考
http://click.aliyun.com/m/16677/
http://blog.csdn.net/watermelonbig/article/details/51116173
http://blog.csdn.net/Tomstrong_369/article/details/53330734
https://www.cnblogs.com/sammyliu/p/4804037.html

###########################