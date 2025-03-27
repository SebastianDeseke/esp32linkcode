from machine import Pin, SoftI2C, I2C, ADC
import ssd1306
import machine
import time, utime, network, json
import onewire, ds18x20
from umqtt.simple import MQTTClient
 
BROKER_ADDRESS = "192.168.1.124"
CLIENT_ID = "ITF221Gr7"
PUBLISH_TOPIC = b"ITF221/7/temperatur"
 
U_AND_P = "ITF221Gr7"
 
SSID = "linksys"
SSID_PASSWORD = "its231LF7"
 
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
 
class Printer:
    curr_line = 1
    lcd: any
 
    def __init__(self):
        self.lcd = ssd1306.SSD1306_I2C(128, 64, SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000))
 
    def write_line(self, input) -> None:
        self.curr_line += 8
        self.lcd.text(input, 1, self.curr_line)
 
    def clear_lines(self) -> None:
        self.curr_line = 1
        self.lcd.fill(0)
 
    def show_lines(self) -> None:
        self.lcd.show()
 
class TemperatureRecorder:
    recorded_temperatures = []
    amount_temperatures: int = 0
    sum_temperatures: float = 0.0
 
    def add_temperature(self, temp: float) -> None:
        self.recorded_temperatures.append(temp)
 
        amount_temperatures = len(self.recorded_temperatures)
 
        if amount_temperatures > MOST_ALLOWED:
            self.recorded_temperatures.pop(0)
            amount_temperatures - 1
 
        self.amount_temperatures = amount_temperatures
        self.sum_temperatures = sum(self.recorded_temperatures)
 
    def get_average(self) -> float:
        if self.amount_temperatures == 0:
            return 0
 
        return round(self.sum_temperatures / self.amount_temperatures, TEMP_DECPLACES)
 
    def eval_tendency(self, temp: float) -> str:
        diff = self.get_average() - temp
 
        if abs(diff) > TEMP_DELTA:
            if diff > 0:
                return "v"
            else:
                return "^"
 
        return "-"
 
    @staticmethod
    def eval_temperature_message(temp: float) -> str:
        if temp > TEMP_HIGH:
            return "zu warm!"
        elif temp < TEMP_LOW:
            return "zu kalt!"
 
        return ""
 
class TemperatureSensor:
    recorder: TemperatureRecorder
    port: int
    recorded_temperatures = []
 
    def __init__(self, port: int, recorder: TemperatureRecorder):
        self.port = port
        self.recorder = recorder
 
    def read_temperature(self) -> float:
        ds = ds18x20.DS18X20(onewire.OneWire(Pin(self.port)))
        roms = ds.scan()
        ds.convert_temp()
        utime.sleep_ms(TEMP_SENSOR_WAIT) # apparently have to wait for convert to finish
 
        for rom in roms:
            temp = round(ds.read_temp(rom), TEMP_DECPLACES)
            self.recorder.add_temperature(temp)
 
            return temp
 
class BrokerManager:
    mqClient: any
 
    def __init__(self, addr, username, password, client_id):
        self.mqClient = MQTTClient(client_id, addr, 1883, username, password, keepalive=0)
        self.mqClient.connect()
 
    def publish(self, msg):
        self.mqClient.publish(PUBLISH_TOPIC, str(msg).encode())
 
    def subscribe(self, topic, fn):
        self.mqClient.set_callback(fn)
        self.mqClient.subscribe(topic)
 
    def poll(self):
        self.mqClient.wait_msg()
 
def display_temperature(topic, msg):
    try:
        msg = msg.decode('utf-8')
        stats = json.loads(msg)
 
        printer.clear_lines()
        printer.write_line("Temperature:")
        printer.write_line(str(stats["temp"]))
        printer.write_line("")
 
        printer.write_line("Average:")
        printer.write_line(str(stats["avg"]))
        printer.write_line("")
 
        printer.show_lines()
    except Exception as e:
        print("Failed to parse message", e)
 
SCAN_INTERVAL = 5
 
do_connect()
 
printer = Printer()
broker = BrokerManager(BROKER_ADDRESS, U_AND_P, U_AND_P, CLIENT_ID)
broker.subscribe(PUBLISH_TOPIC, display_temperature)
 
try:
  while True:
    broker.poll()
 
    time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
          pass
