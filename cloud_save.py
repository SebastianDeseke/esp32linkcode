import network, time
import socket, dht
from machine import Pin

APIKEY = ""
PIN = 14
HOST = "api.thingspeak.com"

def Connect_WiFi ():
    net = network.WLAN(network.STA_IF)
    if not net.isconnected():
        net.activate(True)
        net.connect("", "")
        print(net.ifconfig())

# function to return the temperature and humidity
def TempHum () :
    d = dht.DHT11(Pin(PIN))
    d.measure()
    t = d.temperature()
    h = d.humidity()
    return t, h

# Send data to Thingspeak. (School requirment, but it can be changed to any cloud)
while True:
    Connect_WiFi()
    sock = socket.socket()
    addr = socket.getaddrinfo("api.thingspeak.com", 80)[0][-1]
    sock.connect(addr)
    (t, h) = TempHum()
    host = HOST
    path = "api_key=" + APIKEY + "&field1=" + str(t) + "&field2=" + str(h)
    sock.send(bytes("GET /update?%s HTTP/1.0\r\nHost: %s\r\n\r\n"%(path, host), "utf8"))
    sock.close()
    time.sleep(30)      #Sends the data to the cloud every 30 seconds