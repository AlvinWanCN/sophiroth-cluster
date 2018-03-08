item Name: update_dc.alv.pub_pxe_default

Max # of builds to keep:5

Repository URL: https://github.com/AlvinWanCN/TechnologyCenter.git

Polling ignores commits in certain paths.Included Regions: sophiroth_cluster/pxe_system/conf.d/default

Poll SCM: * * * * *

SSH site: alvin@ansible.alv.pub:22
Command: ssh dc 'sudo curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/pxe_system/conf.d/default > /var/lib/tftpboot/pxelinux.cfg/default'