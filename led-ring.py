import machine, neopixel
import utime

n=16
np=neopixel.NeoPixel(machine.Pin(13), n)

def clear():
    for i in range(n):
        np[i] = (0,0,0)
        np.write

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
    for i in range(n * 4):
        for j in range(n):
            np[j] = (0,0,0)
        np[i % n] = (r,g,b)
        np.write()
        utime.sleep_ms(time)

# execution
def Run (status):
    match status:
        case "success":
            success()
        case "failure":
            failure()
        case "loading":
            loading()
        case _:
            print("An error has occured in identifying the status")