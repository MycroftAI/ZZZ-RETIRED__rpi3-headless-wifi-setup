#!/usr/bin/env python
import threading
from subprocess import Popen, PIPE
from collections import defaultdict
from wifi import Cell, Scheme
import time

class ScanForAP(threading.Thread):
    def __init__(self, name, interface):
        threading.Thread.__init__(self)
        self.name = name
        self.interface = interface
    def run(self):
        ap_scan_results = defaultdict(list)
        try:
            for cell in Cell.all(self.interface):
                ap_scan_results['network'].append({
                    'ssid': cell.ssid,
                    'signal': cell.signal,
                    'quality': cell.quality,
                    'frequency': cell.frequency,
                    'encrypted': cell.encrypted,
                    'channel': cell.channel,
                    'address': cell.address,
                    'mode': cell.mode
                })

            self._return = ap_scan_results
            return 0
        except:
            print "ap scan fail"

    def join(self):
        threading.Thread.join(self)
        return self._return

class JoinAP(threading.Thread):
    def __init__(self, name, interface, ssid, passphrase):
        threading.Thread.__init__(self)
        self.name = name
        self.interface = interface
        self.ssid = ssid
        self.passphrase = passphrase
    def run(self):
        #try:
        #print Cell.all(self.interface)[0]
        cell = Cell.all(self.interface)[0]
        scheme = Scheme.for_cell(self.interface, self.ssid, cell, self.passphrase)
        #scheme.save()
        self._return = scheme.activate()

    def join(self):
        threading.Thread.join(self)
        #return self._return

def bash_command(cmd):
    print cmd
    #try:
    proc = Popen(cmd, shell=True , stdout=PIPE, stderr=PIPE)
    proc.wait()
    #stdout,stderr = proc.communicate()
    #return stderr, proc.returncode

def link_add_vap():
    print bash_command('iw dev wlan0 interface add uap0 type __ap')
    time.sleep(2)
    print bash_command('ifdown upa0')
    time.sleep(2)
    print bash_command('ifup upa0')
    time.sleep(2)
    return

def client_mode_config(iface, ssid, passphrase):
    write_wpa_supplicant_conf(ssid, passphrase)

def client_connect_test(iface, ssid, passphrase):
    print bash_command('wpa_supplicant -iwlan0 -Dnl80211 -c /etc/wpa_supplicant/wpa_supplicant.conf')
    print bash_command('ifdown wlan0')
    print bash_command('ifconfig wlan0 up')
    connect = JoinAP('Connecting to Network', iface, ssid, passphrase)
    #connect.start()
    #connect.join()