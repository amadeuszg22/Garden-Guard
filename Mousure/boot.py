import webrepl
import network
import time
from ntptime import settime
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ama', 'Zaq220991')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
	
do_connect()
time.sleep(1)
settime()
webrepl.start()