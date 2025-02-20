import network, time

def makeWifiPoint(ssid, password):
    net = network.WLAN(network.STA_IF)
    if not net.isconnected():
        net.active(True)
        net.connect(ssid, password)
    else:
        net.disconnect()
        print("Previous connection being terminated...")
        return net
    
    count = 0
    while not net.isconnected() and count < 10:
        time.sleep(1)
        count =+ 1
    try:
        print("Not connected yet")
        time.sleep(1)
    except KeyboardInterrupt:
        pass
    return net


def makeAccessPoint (ssid, password):

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    return ap

def ScanForNetworks ():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    networks = wifi.scan()

    # Print the found networks (a little bit of copilot never hurt no one)
    for network in networks:
        ssid = network[0].decode('utf-8')
        bssid = ':'.join('%02x' % b for b in network[1])
        channel = network[2]
        rssi = network[3]
        print(f"SSID: {ssid}, BSSID: {bssid}, Channel: {channel}, RSSI: {rssi}")

ap = makeAccessPoint("", "")
net = makeWifiPoint("", "")

try:
    while True:
        clientlist = ap.status('stations')
        clientNum = len(clientlist)
        time.sleep(1)

except KeyboardInterrupt:
    pass