

本篇文档讲述ldap用户的添加和删除，<a href=ldapDeploy.md> 部署ldap的步骤请点击这里 </a>


### 1 添加ldap用户和组
这里我们在一个已经搭建好了ldap环境的服务器上添加一个名为diana的用户，密码也是diana

#### Step 1 创建用户并设置密码
```bash
useradd -d /ldapUserData/diana diana #这里因为我们使用的ldap服务在设计上是讲/home/guests/目录作为ldap用户的上级目录，所以diana的目录为 /home/guests/diana
echo diana|passwd diana --stdin
```

#### Step 2 Now filter out these Users and Groups and it password from /etc/shadow to different file:
 ```bash
getent passwd|tail -1 > /root/users
getent shadow|tail -1 > /root/shadow
getent group|tail -1 > /root/groups
```
#### Step 3 Now you need to create ldif file for these users using migrationtools:

```bash
cd /usr/share/migrationtools
./migrate_passwd.pl /root/users > users.ldif
./migrate_group.pl /root/groups > groups.ldif
```


#### Step 4 Upload these users and groups ldif file into LDAP Database:
```bash
 ldapadd -x -W -D "cn=natasha,dc=alv,dc=pub" -f users.ldif
 ldapadd -x -W -D "cn=natasha,dc=alv,dc=pub" -f groups.ldif 
 ##上面的-W参数是交互式输入密码，如果不想交互式输入密码，可以将-W替换为-w,并在-w后面添加ldap管理员密码。
 ##示例：ldapadd -x -w $ldapPassword -D "cn=natasha,dc=alv,dc=pub" -f users.ldif

 ```

### 2 删除用户和组

#### Step1 删除用户
这里我们删除用户natasha
```bash
ldapPassword=your_password
ldapdelete -x -D "cn=natasha,dc=alv,dc=pub" -w $ldapPassword "uid=natasha,ou=People,dc=alv,dc=pub"
```
如果用户信息不对，我们可以通过以下命令来查看相应用户的信息
```bash
ldapsearch -x -b "dc=alv,dc=pub" -H ldap://natasha.alv.pub|grep natasha
```

#### Step2 删除组
```bash
ldapdelete -x -D "cn=natasha,dc=alv,dc=pub" -w $ldapPassword "cn=natasha,ou=Groups,dc=alv,dc=pub"
```
