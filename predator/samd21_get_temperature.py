# CircuitPlaygroundExpress_Temperature
# reads the on-board temperature sensor and prints the value

import time
import array
import math
import adafruit_thermistor
import board
from analogio import AnalogIn
import neopixel

thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE, 10000, 10000, 25, 3950)

analogin = AnalogIn(board.A1)

NUM_SAMPLES = 160

def getVoltage(pin):  # helper
    return ((((pin.value * 3.3) / 65536)/.01)*10-175)

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
    temp_c = thermistor.temperature
    temp_f = thermistor.temperature * 9 / 5 + 32
    votlageN = getVoltage(analogin)
    print("T: %f C and %f F A : %f mV" % (temp_c, temp_f, getVoltage(analogin)))

    time.sleep(0.25)