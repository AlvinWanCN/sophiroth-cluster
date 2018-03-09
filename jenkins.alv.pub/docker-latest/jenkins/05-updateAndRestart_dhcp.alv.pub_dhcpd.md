<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


### 05-updateAndRestart_dhcp.alv.pub_dhcpd item introduction

- [x] item Name

05-updateAndRestart_dhcp.alv.pub_dhcpd

- [x] Max # of builds to keep

5

- [x] Repository URL

https://github.com/AlvinWanCN/sophiroth-cluster.git

- [x] Polling ignores commits in certain paths.Included Regions:

dhcp.alv.pub/dhcpd/conf.d/dhcpd.conf

- [x] Poll SCM:

(* * * * *)

- [x] SSH site

alvin@jenkins.alv.pub:22

- [x] Command

python /opt/jenkins.sophiroth.py 05

- [x] SSH site

alvin@ansible.alv.pub:22

- [x] Command

ansible dhcp -m command -a  'sudo systemctl restart dhcpd'