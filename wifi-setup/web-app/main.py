#!/usr/bin/env python
#!/usr/bin/python

import Queue
import threading
import time
import os
import signal

import tornado.ioloop
import tornado.web, tornado.websocket
import tornado.template
import sys


from server import MainHandler, JSHandler, BootstrapMinJSHandler, BootstrapMinCSSHandler, WSHandler
from WiFiTools import ap_link_tools,dev_link_tools, hostapd_tools
from Config import AppConfig

config = AppConfig()
config.open_file()
Port = config.ConfigSectionMap("server_port")['port']
WSPort = config.ConfigSectionMap("server_port")['ws_port']

linktools = ap_link_tools()
MainHandler.ap = linktools.scan_ap()

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

exitFlag = 0

class tornadoWorker (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        #process_data(self.name, self.q)


        ws_app = tornado.web.Application([(r'/ws', WSHandler), ])
        ws_app.listen('8888')#Port)
        app = tornado.web.Application(handlers, **settings)
        app.listen('80')
        tornado.ioloop.IOLoop.current().start()
        #print "Exiting " + self.name

class stationWorker (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        S = Station()
        S.station_mode_on()
        #process_data(self.name, self.q)
        #print "Exiting " + self.name

class Station():
    def station_mode_on(self):
        aptools = hostapd_tools()
        print "station mode on"
        aptools.hostapd_start()
        aptools.dnsmasq_stop()
        aptools.dnsmasq_start()
        #aptools.ap_config()
# SSP: Temporary change while developing
#        AP.copy_config_ap()
#        devtools.link_down()
#        aptools.ap_up()

    def station_mode_off(self):
        print "station mode off"
        aptools.dnsmasq_stop()
        aptools.hostapd_stop()
# SSP: Temporary change while developing
#        aptools.ap_down()
#        aptools.ap_deconfig()
#        devtools.link_down()
#        devtools.link_up()


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

def exit_gracefully(signal, frame):
    print "caught SIGINT"
    #S.station_mode_off()
    print "exiting"
    sys.exit(0)

nameList = ['web','ap']
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

if __name__ == "__main__":
    ap = linktools.scan_ap()
    signal.signal(signal.SIGINT, exit_gracefully)
    # Create new threads
    #or tName in threadList:
    thread = tornadoWorker (threadID, 'wifi-setup-page-server', workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
    thread = stationWorker(threadID, 'host-ap-server', workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


    # Fill the queue
    queueLock.acquire()
    for word in nameList:
        workQueue.put(word)
    queueLock.release()

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"