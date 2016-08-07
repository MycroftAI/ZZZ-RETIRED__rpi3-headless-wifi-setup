import time
import datetime
import tornado.ioloop
import tornado.web, tornado.websocket
import tornado.template
import os
import re
import ast
import sys
import signal
from subprocess import Popen, PIPE
from threading import Thread
import threading
import logging
from uuid import getnode as get_mac
from hostapdconf import helpers as ha
from hostapdconf.parser import HostapdConf
from shutil import copyfile
from WiFiTools import ap_link_tools,dev_link_tools, hostapd_tools
#from APTools import APConfig
from Config import AppConfig
from operator import itemgetter

#copyfile('config.templates/hostapd.conf.template', '/etc/hostapd/hostapd.conf')
#APConf = HostapdConf('/etc/hostapd/hostapd.conf')
#print APConf['interface']
#APConf['interface'] = 'wlan1'
#print APConf['interface']
#APConf.write()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


def bash_command(cmd):
    print cmd
    try:
        proc = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE)
        stdout,stderr = proc.communicate('n\n')
        #print stderr, proc.returncode
    except:
        print "bash fail"

def Exit_gracefully(signal, frame):
    print "caught SIGINT"
    S.station_mode_off()
    print "exiting"
    sys.exit(0)

class APConfig():
    file_template = 'config.templates/etc/hostapd/hostapd.conf.template'
    file_path = '/etc/hostapd/hostapd.conf'
    interface = 'wlan0'
    driver = 'nl80211'
    ssid = 'PI3-AP'
    hw_mode = 'g'
    channel = 6
    country_code = 'US'
    ieee80211n = 1
    wmm_enabled = 1
    ht_capab = '[HT40][SHORT-GI-20][DSSS_CCK-40]'
    macaddr_acl = 0
    ignore_broadcast_ssid = 0

    def copy_config_ap(self):
        copyfile(self.file_template, self.file_path)
        copyfile('config.templates/etc/dhcpcd.conf.hostapd', '/etc/dhcpcd.conf')
        copyfile('config.templates/etc/default/hostapd.hostapd', '/etc/default/hostapd')
        copyfile('config.templates/etc/dnsmasq.conf.hostapd', '/etc/dnsmasq.conf')
        copyfile('config.templates/etc/network/interfaces.hostapd', '/etc/network/interfaces')


    def write_config(self):
        ha.set_ssid(APConf,self.ssid)
        APConf.write()      

#AP = APConfig()
#APConf = HostapdConf(AP.file_path)

#print AP.file_template
#AP.ssid = "asdfsadfas"
#print AP.ssid
#ha.set_ssid(APConf, AP.ssid)
#AP.write_config()

       

class MainHandler(tornado.web.RequestHandler):
   def get(self):
        self.ap = ap_link_tools().scan_ap()
        print "page loaded", datetime.datetime.now()
        self.render("index.html",
        ap=self.ap)
		
class JSHandler(tornado.web.RequestHandler):
    def get(self):
        print "request for jquery", datetime.datetime.now()
        self.render("jquery-2.2.3.min.js")

class BootstrapMinJSHandler(tornado.web.RequestHandler):
    def get(self):
        print "request for jquery", datetime.datetime.now()
        self.render("bootstrap-3.3.7-dist/js/bootstrap.min.js")

class BootstrapMinCSSHandler(tornado.web.RequestHandler):
    def get(self):
        print "request for jquery", datetime.datetime.now()
        self.render("bootstrap-3.3.7-dist/css/bootstrap.min.css")

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self,origin):
        return True
    def open(self):
        print 'user is connected'

    def on_message(self, message):
        print 'received message: %s\n' % message
        self.write_message(message + ' OK')
        self.message_switch(message)

    def on_close(self):
        print 'connection closed\n'

    def is_match(self, regex, text):
        self.pattern = re.compile(regex)
        return self.pattern.search(text) is not None

    def message_switch(self,message):
        self.dict2 = ast.literal_eval(message)
        print type(self.dict2)
        if self.is_match("'ap_on'", message) is True:
            station_mode_on()
        elif self.is_match("'ap_off'", message) is True:
            station_mode_off()
        elif self.is_match("'scan_networks'", message) is True:
            print "Need: Refresh page/div/unhide/something"
        elif self.is_match("'ssid'", message) is True:
            print "SSID selected: ", self.dict2['ssid']
            wifi_connection_settings['ssid'] = self.dict2['ssid']
        elif self.is_match("'passphrase'", message) is True:
            print "PASSPHRASE Recieved:", self.dict2
            print self.dict2['passphrase']
            # S.station_mode_off()
            wifi_connection_settings['passphrase'] = self.dict2['passphrase']
            connect_to_wifi(wifi_connection_settings['ssid'], self.dict2['passphrase'])

root = os.path.join(os.path.dirname(__file__), "srv/templates")
		
handlers = [
    (r"/", MainHandler),
    (r"/jquery-2.2.3.min.js",JSHandler),
    (r"/img/(.*)", tornado.web.StaticFileHandler, { 'path': os.path.join(root, 'img/') } ),
    (r"/bootstrap-3.3.7-dist/css/bootstrap.min.css",BootstrapMinCSSHandler),
    (r"/bootstrap-3.3.7-dist/js/bootstrap.min.js",BootstrapMinJSHandler),
    (r"/ws",WSHandler)
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "srv/templates"),
)

wifi_connection_settings = {'ssid':'', 'passphrase':''}



def connect_to_wifi(ssid,passphrase):
    print " connecting to wifi:", ssid, passphrase
    template = """country={country}
ctrl_interface=/var/run/wpa_supplicant
update_config=1
network={b1}
    ssid="{ssid}"
    psk="{passphrase}"
    key_mgmt=WPA-PSK
{b2}"""
    context = {
        "b1": '{',
        "b2": '}',
        "country": 'US',
        "ssid": ssid,
        "passphrase": passphrase
    }
    with  open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as myfile:
        myfile.write(template.format(**context))
        myfile.close()
    try:
        bash_command(["ip addr flush wlan0"])
        #bash_command(["wpa_supplicant -iwlan0 -Dnl80211 -c /etc/wpa_supplicant/wpa_supplicant.conf"])
        bash_command(["ifdown","wlan0"])
        #bash_command(['ifconfig', 'wlan0','up'])
        bash_command(["ifup","wlan0"])
    except:
        print "connection failed"
    





if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)

   #threads = []
   #for i in range(5):
    #   t = station_worker()#args=(i,), kwargs={'a': 'A', 'b': 'B'})
    #   t.start()




        #connect_to_wifi(ssid='MOTOROLA-F29E5', passphrase='2e636e8543dc97ee7299')
    #bash_command(['ip', 'addr', 'flush', 'wlan0'])


    # APTools setup
#    AP = APConfig()
#    AP.ssid = 'Mycroft' + '-' + str(get_mac())
#    AP.copy_config_ap()
#    APConf = HostapdConf('/etc/hostapd/hostapd.conf')
#    ha.set_ssid(APConf, AP.ssid)
#    ha.set_iface(APConf, AP.interface)
#    APConf.write()
    config = AppConfig()
    config.open_file()
    Port = config.ConfigSectionMap("server_port")['port']
    WSPort = config.ConfigSectionMap("server_port")['ws_port']
    print Port
    devtools = dev_link_tools()
    #devtools.link_add_vap()
    aptools = hostapd_tools()


##    ap = linktools.scan_ap()
    #W = Wireless()


    #################################################
    # Clean up the list of networks.
    #################################################
    # First, sort by name and strength
##    nets_byNameAndStr = sorted(ap['network'], key=itemgetter('ssid', 'quality'), reverse=True)
    # now strip out duplicates (e.g. repeaters with the same SSID), keeping the first (strongest)
##    lastSSID = "."
##    for n in nets_byNameAndStr[:]:
##        if (n['ssid'] == lastSSID):
##            nets_byNameAndStr.remove(n)
##        else:
##            lastSSID = n['ssid']
    # Finally, sort by strength alone
##        ap['network'] = sorted(nets_byNameAndStr, key=itemgetter('quality'), reverse=True)


    #S = Station()

    #S.station_mode_on()
    ws_app = tornado.web.Application([(r'/ws', WSHandler),])
    ws_app.listen(Port)
    app = tornado.web.Application(handlers, **settings)
    a = Thread(target=app.listen(WSPort))
    tor = Thread(target=tornado.ioloop.IOLoop.current().start())


 #   for i in range(1):
 #       t = threading.Thread(target=station_worker) # args=('work', i, ))
 #       threads.append(t)
 #       t.start()


#    try:
#        print s.is_alive() + "whole lotta debug goin' on"
#        a.start()
#        s.start()
#        t.start()
#    except:
#        sys.exit(1)
