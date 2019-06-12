#!/usr/bin/env python3
# Copyright (c) 2016 John Robinson
# Author: John Robinson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Global Imports
import logging
import time
import Adafruit_GPIO

import sys
import os
sys.path.append("contrib")
#sys.path.append(os.path.join(sys.path[0], "contrib"))
#print(sys.path[0])
# Local Imports
from Adafruit_MAX31856 import MAX31856 as MAX31856

logging.basicConfig(filename='logs/simpletest.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)

# Uncomment one of the blocks of code below to configure your Pi to use software or hardware SPI.

## Raspberry Pi software SPI configuration.
#software_spi = {"clk": 25, "cs": 8, "do": 9, "di": 10}
#sensor = MAX31856(software_spi=software_spi)

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 1
sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Loop printing measurements every second.
#print('Press Ctrl-C to quit.')
#while True:
    #temp = sensor.read_temp_c()
    #internal = sensor.read_internal_temp_c()
    #print('Thermocouple Temperature: {0:0.3F}*C'.format(temp))
    #print('    Internal Temperature: {0:0.3F}*C'.format(internal))
    #time.sleep(1.0)

temp = sensor.read_temp_c()
internal = sensor.read_internal_temp_c()
#string = ""
#if len(sys.argv)>1:
#	string = sys.argv[1]
print('{0:0.1F}'.format(internal) + ' {0:0.1F}'.format(temp))

