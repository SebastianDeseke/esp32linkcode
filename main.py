import time, utime
from machine import Pin, SoftI2C
import onewire, ds18x20


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

# the amount of milliseconds we wait after taking measurements from the 
# temperature sensor. The book uses 750 but that takes quite a while. 
# 100 *should* be fine
TEMP_SENSOR_WAIT = 100

SCAN_INTERVAL = 0.5
IO_PIN = 2

TEMP_DECPLACES = 4
TEMP_LOW = 18
TEMP_HIGH = 22

TEMP_MEAN_INTERVAL = 10
TEMP_DELTA = 1

MOST_ALLOWED = TEMP_MEAN_INTERVAL / SCAN_INTERVAL # most amount of temps we want to keep track of

# printer = Printer()
temp_recorder = TemperatureRecorder()
temp_sensor = TemperatureSensor(IO_PIN, temp_recorder)


try:
  while True:
    temp = temp_sensor.read_temperature()
    temp_message = TemperatureRecorder.eval_temperature_message(temp)

    avg_temp = temp_recorder.get_average()

    tendency = temp_recorder.eval_tendency(temp)

    print("Temperature: ", str(temp), temp_message, "; Avg:", avg_temp, "; Tendency: ", tendency)
    
    time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
          pass