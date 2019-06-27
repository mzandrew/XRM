#!/usr/bin/env python3

# from https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout/python-circuitpython
# pip3 install adafruit-circuitpython-ina260

#import time
import board
import busio
import adafruit_ina260
 
i2c = busio.I2C(board.SCL, board.SDA)
ina260 = adafruit_ina260.INA260(i2c)
I = ina260.current
V = ina260.voltage
print("%.1f %.3f" % (I, V))
#print("Current:", I)
#print("Voltage:", V)
#print("Power:", ina260.power)

