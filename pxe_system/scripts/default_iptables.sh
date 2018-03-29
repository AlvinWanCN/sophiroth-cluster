#!/usr/bin/env bash

iptables -F
iptables -A INPUT -i lo -A ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -s 192.168.0.0/16 -p icmp -j ACCEPT
iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -s 192.168.0.0/16 -p tcp 3306 -j ACCEPT
iptables -A INPUT -s 192.168.0.0/16 -p tcp 10050 -j ACCEPT

iptables -A INPUT -j reject