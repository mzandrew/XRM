#!/usr/bin/env python3

# written 2020-12-15 by mza
# based on B2910-90030.pdf (SCPI-reference)
# and https://socketscpi.readthedocs.io/en/latest/usage.html#socketinstrument
# last updated 2020-12-16 by mza

ip = "192.168.1.2"

import time
import re
import atexit
import socketscpi # sudo pip3 install socketscpi

def setip(desired_ip):
	global ip
	ip = desired_ip

def connect():
	global scpi
	scpi = socketscpi.SocketInstrument(ip, port=5025, timeout=1.0, noDelay=True)
	global connected
	connected = True
	atexit.register(cleanup)

def cleanup():
	global connected
	if connected:
		show_errors()
		scpi.disconnect()
		connected = False

def program(message):
	scpi.write(message)
	#response = query(":SYSTem:ERRor:COUNt?")

def query(message, prefix="", suffix=""):
	response = scpi.query(message)
	print(prefix + response + suffix)
	return response

def identify():
	message = "*IDN?"
	response = scpi.query(message)
	print(response + " at " + ip)

def show_errors():
	query(":SYSTem:ERRor:ALL?")

def get_mode():
	mode = query(":FUNCtion:MODE?")
	return mode

def show_status():
	mode = get_mode()
	if mode=="VOLT":
		get_i()
		get_v()
		get_ilim()
		get_vlim()
	else:
		get_i()
		get_v()
		get_ilim()
		get_vlim()

def on():
	program("OUTp:STAT ON")

def off():
	program("OUTp:STAT OFF")

def get_ilim():
	query(":SENS:CURRent:PROT:LEVel?", "current limit: ", " A")

def get_vlim():
	query(":SENS:VOLTage:PROT:LEVel?", "voltage limit: ", " V")

def get_i():
	query(":MEASure:CURRent?", "current: ", " A")

def get_v():
	query(":MEASure:VOLTage?", "voltage: ", " V")

def set_ilim(desired_ilim):
	program(":SENS:CURRent:PROT:LEVel " + str(desired_ilim))
	get_ilim()

def set_vlim(desired_vlim):
	program(":SENS:VOLTage:PROT:LEVel " + str(desired_vlim))
	get_vlim()

def set_i(desired_i):
	program(":FUNCtion:MODE CURR;:CURRent:LEVel:IMM:AMPL " + str(desired_i))
	get_i()

def set_v(desired_v):
	program(":FUNCtion:MODE VOLT;:VOLTage:LEVel:IMM:AMPL " + str(desired_v))
	get_v()

def set_ilim_v(desired_ilim, desired_v):
	program(":FUNCtion:MODE VOLT;:VOLTage:LEVel " + str(desired_v) + ";:SENS:CURRent:PROT:LEVel " + str(desired_ilim))
	get_ilim()
	get_v()

def set_vlim_i(desired_vlim, desired_i):
	program(":FUNCtion:MODE CURR;:CURRent:LEVel " + str(desired_i) + ";:SENS:VOLTage:PROT:LEVel " + str(desired_vlim))
	get_i()
	get_vlim()

#def sweep_voltage(start_v, end_v, step_v):

def kelvin(mode="query"):
	if mode=="query":
		query(":SENS:REM?")
	else:
		match = re.search("on", mode, re.IGNORECASE)
		if match:
			program(":SENS:REM on")
		match = re.search("off", mode, re.IGNORECASE)
		if match:
			program(":SENS:REM off")

def test():
	#program("*RST")
	#program(":VOLTage:MODE SWE")
	#query(":VOLTage:MODE?")
	#program(":SWE:STA DOUB")
	#query(":SWE:STA?")
	#program(":SWE:DIR UP")
	#query(":SWE:DIR?")
	#program(":FUNC:SHAPe DC")
	#query(":FUNC:SHAPe?")
	#program(":FUNCtion:MODE VOLT")
	#query(":FUNCtion:MODE?")
	#program(":VOLTage:START 9.0")
	#query(":VOLTage:START?")
	#program(":VOLTage:STOP 11.1")
	#query(":VOLTage:STOP?")
	#program(":VOLTage:POIN 201")
	#program(":VOLTage:STEP 0.01")
	#query(":VOLTage:POIN?")
	#query(":VOLTage:STEP?")
	#query(":FUNC:TRIG:CONT?")
	#program(":PULS:DEL 0.01")
	#query(":PULS:DEL?")
	#program(":VOLTage:LEV:IMM:AMPL 8.0")
	#query(":VOLTage:LEV:IMM:AMPL?")
	#program("OUTp:STAT ON")
	#time.sleep(1)
	#query(":CURRent:READ?")
	#time.sleep(1)
	#program("OUTp:STAT OFF")
	#":HCOP:SDUM:DATA?" # screencapture
	#":DISP[:WIND[d]]:DATA?" # return text data from display
	#program(":DISP:TEXT:DATA \"XRM/SLAC/3\"") # 32 char limit
	#query(":DISP:TEXT:DATA?")
	#program(":DISP:TEXT:STAT on")
	#program(":DISP:TEXT:STAT off")
	# ACQuire for measurement, :TRANsient for source output
	#program(":SOUR:VOLT:MODE FIX")
	#program(":SOUR:CURR:MODE FIX")
	#program(":SOUR:SWE:RANG FIX")
	#program(":SOUR:VOLT:RANG:AUTO off")
	#program(":SOUR:VOLT:RANG 20")
	#program(":SOUR:VOLT:MODE LIST")
	#program(":SOUR:LIST:VOLT 9.0, 9.5, 10.0, 10.25, 10.5, 10.75, 11.0, 11.2")
	#steps = 8
	steps = 1000
	stimulus_delay = 0.001
	response_delay = 0.005
	delay = response_delay
	program(":SOURce:FUNCtion:MODE VOLT")
	program(":SOURce:VOLT:MODE swe")
	program(":SOURce:VOLTage:START 9.0")
	program(":SOURce:VOLTage:STOP 11.2")
	program(":SOURce:VOLTage:POIN " + str(steps))
	program(":SOURce:SWEep:SPAC lin")
	#program(":SENS:FUNC \"CURR\",\"SOUR\",\"VOLT\"")
	program(":SENS:FUNC \"CURR\"")
	#program(":SENS:CURR:APER 0.01")
	program(":SENS:CURR:NPLC 0.1")
	program(":SENS:CURR:PROT 1.0")
	program(":TRIG:SOUR AINT")
	#program(":TRIG:TIM 0.01")
	#program(":TRIG:SOUR TIM")
	program(":TRIGger:COUNt " + str(steps))
	program(":TRIGger:TRANsient:DELay " + str(stimulus_delay))
	program(":TRIGger:ACQuire:DELay " + str(response_delay))
	program(":DISP:VIEW graph") # SINGle1|SINGle2|GRAPh|ROLL
	#program(":DISP:VIEW single1") # SINGle1|SINGle2|GRAPh|ROLL
	#query(":DISP:VIEW?")
	#program(":TRIGger:TRANsient:COUNt 2")
	#program(":TRIGger:TRANsient:DELay 0.1")
	#program(":FORM:ELEM:SENS CURR,SOUR")
	query(":SYSTem:ERRor:ALL?")
	program("OUTp:STAT ON")
	#program(":INIT:ACQuire")
	program(":INIT")
	time.sleep(delay * (2*steps+2))
	#program(":INIT:ACQuire")
	#time.sleep(0.4)
	#program(":INIT:ACQuire")
	#time.sleep(0.4)
	#program(":INIT:TRANsient")
	#time.sleep(0.4)
	#query(":IDLE:TRANsient?")
	#program(":INIT:TRANsient")
	#time.sleep(0.4)
	#query(":IDLE:TRANsient?")
	#program(":INIT:TRANsient")
	#time.sleep(0.4)
	#program(":INIT:TRANsient")
	#query(":SENS:DATA?")
	query(":FETCh:ARR:CURR?")
	#program(":INIT:ACQuire")
	#":MMEM:STOR:TRAC file_name"
	#query(":PROG:CAT?")
	#":PROG:PON:COPY name"
	#":PROG:PON:RUN mode"
	#query(":SYST:LFR?") # 50 or 60 [Hz]
	#program(":SYSTem:DATE 2020,12,15")
	#query(":SYSTem:DATE?")
	#program(":SYSTem:TIME 10,34,20")
	#query(":SYSTem:TIME?")
	#query(":SYSTem:LOCK:NAME?")
	#program(":SYSTem:LOCal")
	#program(":SYSTem:LOCK:RELease")
	#query(":SYSTem:LOCK:REQ?")
	#program(":SYSTem:LOCK:RELease")
	query(":SYSTem:ERRor:ALL?")
	#query(":SYSTem:ERRor:COUNt?")
	#program(":SYSTem:LOCK:RELease")
	#":SYST:PON RCL0" # sets power on to recall state 0
	#"*RST" # reset

