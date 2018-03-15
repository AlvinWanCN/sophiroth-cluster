#!/usr/bin/env bash
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/pxe_system/scripts/set_hostname.py)" #根据ip修改主机名
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/pxe_system/scripts/getAnsibleSSHKey.py)" #添加ansible主机ssh public key.
bash -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/disableSeAndFir.sh)" #自定义脚本的方式关闭防火墙
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/pullLocalYum.py)" #添加本地yum仓库
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/joinNatashaLDAP.py)" #加入到我的ldap
sed -i 's/%wheel.*/%wheel  ALL=(ALL) NOPASSWD:  ALL/' /etc/sudoers #设置wheel组nopasswd，便于ansible的操作。
grep /sophiroth/alvin/scripts/welcome.py /etc/profile || echo "/sophiroth/alvin/scripts/welcome.py" >> /etc/profile # 添加登录时执行的脚本。脚本网络地址：https://github.com/AlvinWanCN/scripts/raw/master/python/sophiroth.welcome.py
echo "0 */2 * * * /usr/sbin/ntpdate alv.pub" >> /var/spool/cron/root
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/pxe_system/scripts/resetAnsibleFingerprint.py)" #访问ansible api,修改本服务器的指纹。
python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/$(hostname)/scripts/initial.$(hostname).py)" #每台服务器执行自己相应的配置脚本