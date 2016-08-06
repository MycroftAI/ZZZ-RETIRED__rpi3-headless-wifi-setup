from subprocess import Popen, PIPE
from socket import AF_INET
from pyroute2 import IPRoute
from wifi import Cell, Scheme
from Config import AppConfig
from collections import defaultdict
from wireless import Wireless

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

# wifi schem


class ap_link_tools():
    def __init_(self):
        pass
    def scan_ap(self):
        print "Availible links:", self.scan_links()
        interface = config.ConfigSectionMap("wifi-ap")['iface']
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
    def dnsmasq_start(self):
        print "start dnsmasq"
        bash_command(["systemctl", "start", "dnsmasq.service"])
        #bash_command(["dnsmasq",  "--interface=uap0", "--dhcp-range=uap0,172.24.1.1,172.24.1.1,255.255.255.0"])
    def dnsmasq_stop(self):
        print "stop dnsmasq"
        bash_command(["systemctl", "stop", "dnsmasq.service"])

    def hostapd_start(self):
        bash_command(["systemctl", "start", "hostapd.service"])

    def hostapd_stop(self):
        bash_command(['systemctl', 'stop', 'hostapd.service'])


class dev_link_tools():
#    interface = config.ConfigSectionMap("wifi")['iface']
    def __init__(self):
        pass

    def link_add(self):
        interface = config.ConfigSectionMap("wifi-ap")['iface']
        dev = ip.link_lookup(ifname=link)[0]

    def link_up(self, link):
        interface = config.ConfigSectionMap("wifi-ap")['iface']
        dev = ip.link_lookup(ifname=link)[0]
        ip.link('set', index=dev,
            state='up')

    def link_down(self, link):
        interface = config.ConfigSectionMap("wifi-ap")['iface']
        dev = ip.link_lookup(ifname=interface)[0]
        ip.link('set', index=dev,
            state='down')
    def link_add_vap(self):
        bash_command('iw dev wlan0 interface add uap0 type __ap')
        bash_command('ifdown upa0')
        bash_command('ifup upa0')

def bash_command(cmd):
    print cmd
    #try:
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout,stderr = proc.communicate()
    return stdout, stderr, proc.returncode


    #except stderr:
        #print stdout, stderr
