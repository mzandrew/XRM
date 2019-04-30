#!/usr/bin/env python

# written 2019-04-30 by mza
# last updated 2019-04-30 by mza

#if __name__ == "__main__":
import sys
if len(sys.argv) < 2:
	filename = "/dev/stdin"
else:
	filename = sys.argv[1]
#print filename
lines = []
for line in open(filename):
	line = line.rstrip("\n\r")
	lines.append(line)
print "read " + str(len(lines)) + " lines from file " + filename
import re
#events = {}
input_energies = {}
deposited_energies = {}
for line in lines:
	match = re.search("^([0-9]+) +([.e0-9-]+) +([.e0-9-]+)$", line)
	if match:
		#print line
		event_number = int(match.group(1))
		input_energy = float(match.group(2))
		deposited_energy = float(match.group(3))
		#print str(event_number) + " " + str(input_energy) + " " + str(deposited_energy)
		#events[event_number] = (input_energy, deposited_energy)
		input_energies[event_number] = input_energy
		deposited_energies[event_number] = deposited_energy

import ROOT
canvas1 = ROOT.TCanvas('canvas1', 'mycanvas', 100, 50, 800, 600)
canvas1.SetLogx()
number_of_bins = 100
low = 0.004
high = 60.
import math
factor = 10.**(math.log10(high/low)/number_of_bins)
#print str(factor)
bin_widths = []
bin_widths.append(low)
for i in range(number_of_bins - 1):
	bin_widths.append(bin_widths[i]*factor)
bin_widths.append(high)
#print len(bin_widths)
#print str(number_of_bins)
#print bin_widths
import numpy
fbin_widths = numpy.array(bin_widths, dtype='float64')
#import sys
#sys.exit(1)
#histogram1 = ROOT.TH1F('histogram1', 'mytitle', number_of_bins, 0.004, 60)
histogram1 = ROOT.TH1F('histogram1', filename, number_of_bins, fbin_widths)
#histogram1.SetDrawOption("G")
#for event in input_energies.keys():
#	histogram1.Fill(input_energies[event])
for event in deposited_energies.keys():
	histogram1.Fill(deposited_energies[event])
histogram1.GetXaxis().SetTitle("deposited energy [keV]")
histogram1.GetYaxis().SetTitle("number of events")
#normalization = histogram1.GetEntries()
#histogram1.Scale(1./normalization)
#histogram1.GetYaxis().SetTitle("relative abundance")
histogram1.Draw()
canvas1.Update()

if len(sys.argv) < 2:
	import time
	time.sleep(1)
else:
	#raw_input("Press Enter to continue...")
	imagefile = ROOT.TImage.Create()
	imagefile.FromPad(canvas1)
	imagefile.WriteImage(filename + ".png")

