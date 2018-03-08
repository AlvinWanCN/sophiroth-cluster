<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

### ansible installation
```bash
# cat >/etc/yum.repos.d/centos7-extras.repo<<EOF
[centos7extras]
name=centos7-extras
baseurl=http://mirrors.aliyun.com/centos/7/extras/x86_64/
gpgcheck=0
enabled=1
EOF
# yum install ansible -y
```

### ansible configuraion

- step 1, make ssh key

```bash
# ssh-keygen #enter enter enter

```

- step 2, push ssh public key to destination host </br>
example host is db1.alv.pub and db2 </br>
```bash
# ssh-copy-id -i ~/.ssh/id_rsa.pub db1.alv.pub
# ssh-copy-id -i ~/.ssh/id_rsa.pub db2.alv.pub
```

- step 3, config host or group

```bash
# vim /etc/ansible/hosts
[dbs] #group name
db1.alv.pub  #hostname
db2.alv.pub:22 #指定22端口
```

- step 4, use ansible.

we test ping mudule
```bash
ansible db1.alv.pub -m ping
ansible db2.alv.pub -m ping 
ansible dbs -m ping

```
