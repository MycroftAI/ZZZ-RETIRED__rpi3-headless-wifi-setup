#!/bin/bash
echo "this is ap-up.sh"
bash -x config-change-ap-on.sh
ifdown wlan0
service dnsmasq start
service dhcpcd restart
/usr/sbin/hostapd /etc/hostapd/hostapd.conf 
#python ../wifi-setup.py &
iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p tcp -m tcp --dport 80 -j DNAT --to-destination 172.24.1.1:80
#iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p tcp -m tcp --dport 433 -j DNAT --to-destination 172.24.1.1:80
iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p udp -m udp --dport 53 -j DNAT --to-destination 172.24.1.1:53
