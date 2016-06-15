#!/bin/bash
echo "this is ap-down.sh"
#bash -x config-change-restore.sh
service dnsmasq stop
service dhcpcd restart
service networking restart
#ifdown wlan0
ip addr flush wlan0
#ifup wlan0

#/usr/sbin/hostapd /etc/hostapd/hostapd.conf
