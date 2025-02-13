import network, time

def makeAccessPoint():
    ssid = 'WiFi_abc'
    password = '1'

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    return ap

ap = makeAccessPoint()

try:
    while True:
        clientlist = ap.status('stations')
        clientNum = len(clientlist)
        time.sleep(1)

except KeyboardInterrupt:
    pass