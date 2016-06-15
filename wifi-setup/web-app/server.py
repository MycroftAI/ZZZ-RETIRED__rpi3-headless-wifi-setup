import time
import datetime
import tornado.ioloop
import tornado.web, tornado.websocket
import tornado.template
import os
import re
import ast
from WiFiTools import ap_link_tools, dev_link_tools,hostapd_tools
from Config import AppConfig


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "page loaded", datetime.datetime.now()
        self.render("index.html",
        ap=ap)

class JSHandler(tornado.web.RequestHandler):
    def get(self):
        print "request for jquery", datetime.datetime.now()
        self.render("jquery-2.2.3.min.js")

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
    (r"/ws",WSHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "srv/templates"),
)

wifi_connection_settings = {'ssid':'', 'passphrase':''}

def station_mode_on():
    print "station mode on"
#    aptools.ap_config()
#    devtools.link_down()
#    aptools.ap_up()

def station_mode_off():
    print "station mode off"
#    aptools.ap_down()
#    aptools.ap_deconfig()
#    devtools.link_down()
#    devtools.link_up()

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
        station_mode_off()
        wifi_connection_settings['passphrase'] = dict2['passphrase']
        connect_to_wifi(wifi_connection_settings['ssid'],dict2['passphrase'])
#        time.sleep(5)

def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None

if __name__ == "__main__":
    config = AppConfig()
    config.open_file()
    Port = config.ConfigSectionMap("server_port")['port']
    WSPort = config.ConfigSectionMap("server_port")['ws_port']
    print Port
    linktools = ap_link_tools()
    devtools = dev_link_tools()
    aptools = hostapd_tools()
    ap = linktools.scan_ap()
    ws_app = tornado.web.Application([(r'/ws', WSHandler),])
    ws_app.listen(Port)
    app = tornado.web.Application(handlers, **settings)
    app.listen(WSPort)
    tornado.ioloop.IOLoop.current().start()

