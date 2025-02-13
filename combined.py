import network, time
import machine, neopixel
import utime

def makeAccessPoint():
    ssid = 'WiFi_abc'
    password = '1'

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    return ap

n=12
np=neopixel.NeoPixel(machine.Pin(12), n)

def clear():
    for i in range(n):
        np[i] = (0,0,0)
    np.write()

# set colour method
def set_colour (r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()

# success
def success ():
    #lawngreen
    set_colour (124,252,0)

# failure
def failure ():
    #firebrick
    set_colour(178,34,34)

# loading
def loading ():
    #yellow
    cycle(255,255,0,250)

# cycle
def cycle (r, g, b, time):
    for i in range(n):
        for j in range(n):
            np[j] = (0,0,0)
        np[i % n] = (r,g,b)
        np.write()
        utime.sleep_ms(time)


ap = makeAccessPoint()

try:
    while True:
        clientlist = ap.status('stations')
        clientNum = len(clientlist)
        if clientNum > 0:
            success()
        else:
            loading()
        time.sleep(1)
except KeyboardInterrupt:
    failure()
    time.sleep(1)
    clear()
    pass