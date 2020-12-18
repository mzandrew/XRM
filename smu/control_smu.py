#!/usr/bin/env python3

# written 2020-12-16 by mza
# last updated 2020-12-18 by mza

# keysign B2901A:
ip = "192.168.22.40"

# SLAC sensors:
ilim = 10.0e-3
v = 30.0

import time
import sys
import re
import b2901a
from DebugInfoWarningError24 import debug, info, warning, error, debug2, debug3, set_verbosity, create_new_logfile_with_string

# led strip for testing:
vlim = 11.1
ilim = 1.0
v = 11.1
i = 1.00

#b2901a.set_v(10.587654321)
#b2901a.set_ilim(0.2)
#b2901a.set_ilim_v(0.3, 11)
#time.sleep(1)
#b2901a.set_vlim_i(vlim, i)

if __name__ == "__main__":
	create_new_logfile_with_string("control_smu")
	b2901a.setip(ip)
	b2901a.connect()
	if len(sys.argv) > 1:
		command = ""
		#debug(str(len(sys.argv)))
		for arg in sys.argv[1:]:
			#debug(arg)
			match = re.search("(on|off)", arg, re.IGNORECASE)
			if match:
				command = match.group(1)
				debug("matched " + command)
		if not command=="":
			match = re.search("on", command, re.IGNORECASE)
			if match:
				info("turning on")
				b2901a.set_ilim_v(ilim, v)
				b2901a.on()
			match = re.search("off", command, re.IGNORECASE)
			if match:
				info("turning off")
				b2901a.off()
	else:
		#b2901a.identify()
		#b2901a.show_status()
		b2901a.print_header()
		while True:
			b2901a.compact_status()
			sys.stdout.flush()
			time.sleep(1)

#b2901a.kelvin("on")
#time.sleep(1)
#b2901a.get_i()
#b2901a.get_v()
#b2901a.kelvin("off")
#time.sleep(1)
#b2901a.get_i()
#b2901a.get_v()
#b2901a.kelvin()

#$ ./control_smu.py
#Keysight Technologies,B2901A,MY51144054,3.4.1910.3210 at 192.168.22.40
#VOLT
#current: +9.760740E-01 A
#voltage: +1.105996E+01 V
#current limit: +1.00000000E+000 A
#voltage limit: +1.11000000E+001 V
#+0,"No error"

