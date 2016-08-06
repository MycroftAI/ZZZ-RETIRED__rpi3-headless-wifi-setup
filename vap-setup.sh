#!/usr/bin/env bash

#bash +x $(iw dev wlan0 interface add uap0 type __ap)
service dnsmasq stop
ifdown uap0
ifup uap0
dnsmasq -d --interface=uap0 --dhcp-range=uap0,172.24.1.1,172.24.1.1,255.255.255.0
