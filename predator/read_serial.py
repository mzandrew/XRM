#!/usr/bin/env python3

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

cc=str(ser.readline())
print(cc)

