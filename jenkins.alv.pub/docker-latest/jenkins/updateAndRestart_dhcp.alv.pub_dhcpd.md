<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


### updateAndRestart_dhcp.alv.pub_dhcpd item introduction

- [x] item Name

updateAndRestart_dhcp.alv.pub_dhcpd

- [x] Max # of builds to keep

5

- [x] Repository URL

https://github.com/AlvinWanCN/TechnologyCenter.git

- [x] Polling ignores commits in certain paths.Included Regions:

sophiroth_cluster/dhcp.alv.pub/dhcpd.conf

- [x] Poll SCM:

(* * * * *)

- [x] SSH site

alvin@ansible.alv.pub:22

- [x] Command

ssh dhcp 'sudo python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/sophiroth_cluster/dhcp.alv.pub/dhcpd/scripts/updateDhcpd.py)"'