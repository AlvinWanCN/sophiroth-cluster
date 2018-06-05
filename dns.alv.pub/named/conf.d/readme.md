## Server
natasha.alv.pub
##Function
dns service.
## Configuration file full address

/etc/named.conf </br>
/etc/named.rfc1912.zones </br>
/var/named/alv.pub.zone </br>
/var/named/shenmin.com.zone </br>

- [x] Provide update dns command at ansible.
```bash
ansible alv.pub -m command -a 'sudo python -c "$(curl -fsSL https://github.com/AlvinWanCN/TechnologyCenter/raw/master/sophiroth_cluster/alv.pub/named/update.named.alv.pub.py)"'
```