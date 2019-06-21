# CircuitPlaygroundExpress_Temperature
# reads the on-board temperature sensor and prints the value

import board
import digitalio
import sys
import time
import array
import math
import adafruit_thermistor
import analogio

def getVoltage(pin):
    return pin.value * 3.3 / 65536.0

def getCurrent(pin):  # helper
    R = 0.01
    gain = 10.0
    #return ((((pin.value * 3.3) / 65536)/R)*10-175)
    return (getVoltage(pin)/gain/R)

#def mean(values):
#    return sum(values) / len(values)

#def normalized_rms(values):
#    minbuf = int(mean(values))
#    samples_sum = sum(
#        float(sample - minbuf) * (sample - minbuf)
#        for sample in values
#    )
#    return math.sqrt(samples_sum / len(values))

#samples = array.array('H', [0] * NUM_SAMPLES)
#input_floor = normalized_rms(samples) + 10

initialized = False

def init():
    global thermistor
    global initialized
    if initialized:
        #print("already initialized")
        return 0
    #print("initializing thermistor")
    thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
    initialized = True

def main():
    try:
        init()
        soft_boot = digitalio.DigitalInOut(board.D4)
        soft_boot.direction = digitalio.Direction.INPUT
        soft_boot.pull = digitalio.Pull.DOWN
        led = digitalio.DigitalInOut(board.D13)
        led.direction = digitalio.Direction.OUTPUT
        #led.value = True
        analog0 = analogio.AnalogIn(board.A0)
        analog1 = analogio.AnalogIn(board.A1)
        #import neopixel
        #NUM_SAMPLES = 160
        #pixel = neopixel.NeoPixel(board.A1, 8, 0.3, True)
        #pixel.fill(0, 0, 255)
        #time.sleep(0.25)
        reporting_frequency = 1.0 # Hz
        log2_of_number_of_acquisitions_to_accumulate = 8
        number_of_acquisitions_to_accumulate = 2.0 ** log2_of_number_of_acquisitions_to_accumulate
        #print(str(number_of_acquisitions_to_accumulate))
        if number_of_acquisitions_to_accumulate < 1:
            return 1
        short_timestep = 1.0 / number_of_acquisitions_to_accumulate / reporting_frequency # s
        #print(str(short_timestep))
        #long_timestep  = short_timestep * number_of_acquisitions_to_accumulate / reporting_frequency# s
        while True:
            led.value = not led.value
            #pixel.fill(0, 255, 0)
            #time.sleep(0.25)
            #temp_f = thermistor.temperature * 9.0 / 5.0 + 32.0
            #votlageN = getVoltage(analogin)
            #print("T: %f C and %f F A : %f mV" % (temp_c, temp_f, getVoltage(analogin)))
            #print("%.1f %.3f" % (temp_c, getCurrent(analogin)))
            temp_c = 0.0
            v0 = 0.0
            v1 = 0.0
            for i in range(0, number_of_acquisitions_to_accumulate):
                temp_c += thermistor.temperature
                v0 += getVoltage(analog0)
                v1 += getVoltage(analog1)
                time.sleep(short_timestep)
                if soft_boot.value:
                    try:
                        soft_boot.deinit()
                    except:
                        pass
                    try:
                        led.deinit()
                    except:
                        pass
                    try:
                        analog0.deinit()
                    except:
                        pass
                    try:
                        analog1.deinit()
                    except:
                        pass
                    return 0
            #temp_c >>= log2_of_number_of_acquisitions_to_accumulate
            #v0 >>= log2_of_number_of_acquisitions_to_accumulate
            #v1 >>= log2_of_number_of_acquisitions_to_accumulate
            temp_c /= number_of_acquisitions_to_accumulate
            v0 /= number_of_acquisitions_to_accumulate
            v1 /= number_of_acquisitions_to_accumulate
            diff = 1000.0 * (v1 - v0)
            print("%.1f %.3f %.3f %.3f" % (temp_c, v0, v1, diff))
            #pixel.fill(255, 0, 0)
            #time.sleep(long_timestep)
    except:
        print("got unhandled exception in samd21_get_temperature.py")
        try:
            soft_boot.deinit()
        except:
            pass
        try:
            led.deinit()
        except:
            pass
        try:
            analog0.deinit()
        except:
            pass
        try:
            analog1.deinit()
        except:
            pass
        time.sleep(1)
        return 0

if __name__ == '__main__':
    main()

