import time
import datetime
import tornado.ioloop
import tornado.web, tornado.websocket
import tornado.template
import os
import re
import ast
from threading import Thread
from uuid import getnode as get_mac
from hostapdconf import helpers as ha
from hostapdconf.parser import HostapdConf
from shutil import copyfile
from WiFiTools import ap_link_tools, dev_link_tools,hostapd_tools
#from APTools import APConfig
from Config import AppConfig

#copyfile('config.templates/hostapd.conf.template', '/etc/hostapd/hostapd.conf')
#APConf = HostapdConf('/etc/hostapd/hostapd.conf')
#print APConf['interface']
#APConf['interface'] = 'wlan1'
#print APConf['interface']
#APConf.write()

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
        print "page loaded", datetime.datetime.now()
        self.render("index.html",
        ap=ap)
		
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
        message_switch(message)

    def on_close(self):
        print 'connection closed\n'

handlers = [
    (r"/", MainHandler),
    (r"/jquery-2.2.3.min.js",JSHandler),
    (r"/img/(.*)", tornado.web.StaticFileHandler, { 'path': r'img/' } ),
    (r"/bootstrap-3.3.7-dist/css/bootstrap.min.css",BootstrapMinCSSHandler),
    (r"/bootstrap-3.3.7-dist/js/bootstrap.min.js",BootstrapMinJSHandler),
    (r"/ws",WSHandler)
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "srv/templates"),
)

wifi_connection_settings = {'ssid':'', 'passphrase':''}

class station(Thread):
    def station_mode_on(self):
        print "station mode on"
        #aptools.ap_config()
# SSP: Temporary change while developing		
#        AP.copy_config_ap()
#        devtools.link_down()
#        aptools.ap_up()

    def station_mode_off(self):
        print "station mode off"
# SSP: Temporary change while developing		
#        aptools.ap_down()
#        aptools.ap_deconfig()
#        devtools.link_down()
#        devtools.link_up()

def connect_to_wifi(ssid,passphrase):
    print " connecting to wifi:", ssid, passphrase
    
def message_switch(message):
    dict2 = ast.literal_eval(message)
    print type(dict2)
    if is_match("'ap_on'", message) is True:
        station_mode_on()
    elif is_match("'ap_off'", message) is True:
        station_mode_off()
    elif is_match("'scan_networks'", message) is True:
        print "Need: Refresh page/div/unhide/something"
    elif is_match("'ssid'", message) is True:
        print "SSID selected: ", dict2['ssid']
        wifi_connection_settings['ssid'] = dict2['ssid']
    elif is_match("'passphrase'",message) is True:
        print "PASSPHRASE Recieved:", dict2
        print dict2['passphrase']
        S.station_mode_off()
        wifi_connection_settings['passphrase'] = dict2['passphrase']
        connect_to_wifi(wifi_connection_settings['ssid'],dict2['passphrase'])
#        time.sleep(5)

def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None


if __name__ == "__main__":
    # APTools setup
    AP = APConfig()
    AP.ssid = 'Mycroft' + '-' + str(get_mac())
    AP.copy_config_ap()
    APConf = HostapdConf('/etc/hostapd/hostapd.conf')
    ha.set_ssid(APConf, AP.ssid)
    ha.set_iface(APConf, AP.interface)
    APConf.write()
    config = AppConfig()
    config.open_file()
    Port = config.ConfigSectionMap("server_port")['port']
    WSPort = config.ConfigSectionMap("server_port")['ws_port']
    print Port
    linktools = ap_link_tools()
    devtools = dev_link_tools()
    aptools = hostapd_tools()
    ap = linktools.scan_ap()
    S = station()
#    t = Thread(target=S.station_mode_on())
    #station_mode_on()
    ws_app = tornado.web.Application([(r'/ws', WSHandler),])
    ws_app.listen(Port)
    app = tornado.web.Application(handlers, **settings)
    app.listen(WSPort)
    t2 =Thread(target=tornado.ioloop.IOLoop.current().start())
    tornado.ioloop.IOLoop.current().start()
    try:
        t.start()
        t.join()
    except:
        sys.exit()
