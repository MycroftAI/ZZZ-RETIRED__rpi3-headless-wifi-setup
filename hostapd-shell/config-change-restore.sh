#!/bin/bash
echo "restoring '/etc/dhcpcd.conf' to original" 
cat ./hostapd-shell/config/etc/dhcpcd.conf.orig > /etc/dhcpcd.conf
echo "restoring '/etc/network/interfaces' to original" 
cat ./hostapd-shell/config/etc/network/interfaces.orig > /etc/network/interfaces
echo "restoring /etc/default/hostapd"
cat ./hostapd-shell/config/etc/default/hostapd.orig > /etc/default/hostapd
echo "restoring /etc/dnsmasq.conf"
cat ./hostapd-shell/config/etc/dnsmasq.conf.orig > /etc/dnsmasq.conf
echo "deleting /etc/hostapd/hostapd.conf"
rm /etc/hostapd/hostapd.conf

