#!/bin/bash
TOP=${PWD}
echo "this is ap-up.sh"
bash -x ${TOP}/config-change-ap-on.sh
ifdown wlan0
ifconfig wlan0 up
#/usr/sbin/dnsmasq -C /etc/dnsmasq.conf
systemctl start dnsmasq.service
systemctl start dhcpcd.service
/usr/sbin/hostapd /etc/hostapd/hostapd.conf &
#python ../wifi-setup.py &
iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p tcp -m tcp --dport 80 -j DNAT --to-destination 172.24.1.1:80
#iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p tcp -m tcp --dport 433 -j DNAT --to-destination 172.24.1.1:80
iptables -t nat -A PREROUTING -s 172.24.1.0/255.255.255.0 -p udp -m udp --dport 53 -j DNAT --to-destination 172.24.1.1:53
