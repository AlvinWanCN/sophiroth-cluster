<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


- [x] item Name:
 
 04-updateAndReload_dns.alv.pub_named
 

- [x] Max # of builds to keep

5

- [x] Repository URL
 
https://github.com/AlvinWanCN/sophiroth-cluster.git

- [x]  Polling ignores commits in certain paths.Included Regions

dns.alv.pub/named/conf.d/alv.pub.zone

- [x] Poll SCM

(* * * * *)

- [x] SSH site: 

alvin@dns.alv.pub:xxx

- [x] Command

sudo python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/scripts/update.named.dns.alv.pub.py)"