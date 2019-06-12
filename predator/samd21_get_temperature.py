# CircuitPlaygroundExpress_Temperature
# reads the on-board temperature sensor and prints the value

import board

import digitalio
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = True

import time
import array
import math
import adafruit_thermistor
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
from analogio import AnalogIn
analog0 = AnalogIn(board.A0)
analog1 = AnalogIn(board.A1)
#import neopixel

NUM_SAMPLES = 160

#pixel = neopixel.NeoPixel(board.A1, 8, 0.3, True)
#pixel.fill(0, 0, 255)
#time.sleep(0.25)

def getVoltage(pin):
    return pin.value * 3.3 / 65536.0

def getCurrent(pin):  # helper
    R = 0.01
    gain = 10.0
    #return ((((pin.value * 3.3) / 65536)/R)*10-175)
    return (getVoltage(pin)/gain/R)

def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
    return math.sqrt(samples_sum / len(values))

samples = array.array('H', [0] * NUM_SAMPLES)
input_floor = normalized_rms(samples) + 10

while True:
    led.value = not led.value
    #pixel.fill(0, 255, 0)
    #time.sleep(0.25)
    temp_c = thermistor.temperature
    #temp_f = thermistor.temperature * 9.0 / 5.0 + 32.0
    #votlageN = getVoltage(analogin)
    #print("T: %f C and %f F A : %f mV" % (temp_c, temp_f, getVoltage(analogin)))
    #print("%.1f %.3f" % (temp_c, getCurrent(analogin)))
    print("%.1f %.3f %.3f" % (temp_c, getVoltage(analog0), getVoltage(analog1)))
    #pixel.fill(255, 0, 0)
    time.sleep(0.25)

