import subprocess
from socket import AF_INET
from pyroute2 import IPRoute
from wifi import Cell, Scheme
from Config import AppConfig
from collections import defaultdict

#app_config = './configuration/default.ini'

#config = AppConfig()
#ip = IPRoute()

#config.open_file(app_config)
#config.create_section('wifi')
#config.set_option('wifi','iface','wlan0')
#config.set_option('wifi','iface','wlp3s0')
#config.write_file(app_config)
config = AppConfig()
ip = IPRoute()

class ap_link_tools():
    def __init_(self):
        pass
    def scan_ap(self):
        print "Availible links:", self.scan_links()
        interface = config.ConfigSectionMap("wifi")['iface']
        print "Configured link:", interface
        aplist = defaultdict(list)
        for cell in Cell.all(interface):
            aplist['network'].append({
                'ssid': cell.ssid,
                'signal': cell.signal,
                'quality': cell.quality,
                'frequency': cell.frequency,
                'encrypted': cell.encrypted,
                'channel': cell.channel,
                'address': cell.address,
                'mode': cell.mode
            })
        return aplist

    def scan_links(self):
        return [x.get_attr('IFLA_IFNAME') for x in ip.get_links()]

class hostapd_tools():
    def ap_config(self):
        bash_command('bash -x /home/pi/rpi3-headless-wifi-setup/hostapd-shell/config-change-ap-on.sh')
    def ap_deconfig(self):
        bash_command('bash -x  /home/pi/rpi3-headless-wifi-setup/hostapd-shell/config-change-restore.sh')
    def ap_up(self):
        bash_command('bash -x /home/pi/rpi3-headless-wifi-setup/hostapd-shell/ap-up.sh')
    def ap_down(self):
        bash_command('bash -x /home/pi/rpi3-headless-wifi-setup/hostapd-shell/ap-down.sh')

class dev_link_tools():
#    interface = config.ConfigSectionMap("wifi")['iface']
    def __init__(self):
        pass

    def link_add(self):
        interface = config.ConfigSectionMap("wifi")['iface']
        dev = ip.link_lookup(ifname=interface)[0]

    def link_up(self):
        interface = config.ConfigSectionMap("wifi")['iface']
        dev = ip.link_lookup(ifname=interface)[0]
        ip.link('set', index=dev,
            state='up')

    def link_down(self):
        interface = config.ConfigSectionMap("wifi")['iface']
        dev = ip.link_lookup(ifname=interface)[0]
        ip.link('set', index=dev,
            state='down') 

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')
 
