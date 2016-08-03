#!/bin/bash
echo "overwriting '/etc/dhcpcd.conf' for hostap mode" 
cat config/etc/dhcpcd.conf.hostap > /etc/dhcpcd.conf
echo "overwriting '/etc/network/interfaces' for hostap mode" 
cat config/etc/network/interfaces.hostap > /etc/network/interfaces
echo "overwriting /etc/default/hostapd"
cat config/etc/default/hostapd.hostap > /etc/default/hostapd
echo "writing /etc/hostapd/hostapd.conf"
cat config/etc/hostapd/hostapd.conf > /etc/hostapd/hostapd.conf
echo "overwriting /etc/dnsmasq.conf"
cat config/etc/dnsmasq.conf.hostap > /etc/dnsmasq.conf
