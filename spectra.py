#!/usr/bin/env python

import os # path, environ
import sys # path, exit, argv
#sys.path.append(ps.path.join(os.path.expanduser("~"), "/build/root/lib"))
try:
	import ROOT # TH1F
except:
	print "ROOT environment not setup yet"
	HOME = os.environ['HOME']
	#print ". " + HOME + "/build/root/bin/thisroot.sh; " + str(sys.argv)
	print ". " + HOME + "/build/root/bin/thisroot.sh"
	print sys.argv[0] + " ..."
	sys.exit(1)
import re # search
import math # log10
import numpy # float array

# written 2019-04-30 by mza
# last updated 2019-05-03 by mza

number_of_bins = 1000
low = 0.004
high = 50.
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
fbin_widths = numpy.array(bin_widths, dtype='float64')

J_per_eV = 1.60217733e-19
J_per_MeV = 1.0e6 * J_per_eV
bunches_per_second = 508.8875e6

def show_energy_per_bunch_and_power():
	print "total_energy_incident " + str(total_energy_incident_eV/1.e6) + " MeV per bunch"
	print "total_energy_deposited " + str(total_energy_deposited_eV/1.e6) + " MeV per bunch"
	total_energy_incident_J = J_per_MeV * total_energy_incident_eV / 1.e6
	total_energy_deposited_J = J_per_MeV * total_energy_deposited_eV / 1.e6
	print "total_energy_incident " + str(total_energy_incident_J) + " J per bunch"
	print "total_energy_deposited " + str(total_energy_deposited_J) + " J per bunch"
	total_power_incident_W = total_energy_incident_J * bunches_per_second
	total_power_deposited_W = total_energy_deposited_J * bunches_per_second
	print "total_power_incident " + str(total_power_incident_W) + " W"
	print "total_power_deposited " + str(total_power_deposited_W) + " W"

legend1 = ROOT.TLegend(0.1, 0.75, 0.45, 0.9)
#if __name__ == "__main__":
filenames = []
import sys
png_filename = "XRM.png"
if len(sys.argv) < 2:
	filenames.append("/dev/stdin")
else:
	png_filename = sys.argv[1]
	for each in sys.argv[2:]:
		filenames.append(each)
histograms = []
i = 0
title = " vs ".join(filenames)
histogram_stack = ROOT.THStack("histogram_stack", title)
lines = 0
for filename in filenames:
	#print filename
	#lines = []
	#for line in open(filename):
	#	line = line.rstrip("\n\r")
	#	lines.append(line)
	#input_energies_eV = {}
	#deposited_energies_eV = {}
	total_energy_incident_eV = 0.0
	total_energy_deposited_eV = 0.0
	histograms.append(ROOT.TH1F('histogram['+str(i)+']', title, number_of_bins, fbin_widths))
	for line in open(filename):
		line = line.rstrip("\n\r")
		match = re.search("^([0-9]+) +([.e0-9-]+) +([.e0-9-]+)$", line)
		if match:
			#print line
			#event_number = int(match.group(1))
			input_energy_eV = float(match.group(2))
			deposited_energy_eV = float(match.group(3))
			total_energy_incident_eV += input_energy_eV
			total_energy_deposited_eV += deposited_energy_eV
			#print str(event_number) + " " + str(input_energy) + " " + str(deposited_energy)
			#input_energies_eV[event_number] = input_energy_eV
			#deposited_energies_eV[event_number] = deposited_energy_eV
			histograms[i].Fill(deposited_energy_eV/1000.0)
		lines = lines + 1
	print "read " + str(lines) + " lines from file " + filename
	show_energy_per_bunch_and_power()
	#for event in input_energies.keys():
	#	histograms[i].Fill(input_energies[event])
	#for event in deposited_energies_eV.keys():
	legend1.AddEntry(histograms[i], filename + " (" + str(int(histograms[i].GetEntries())) + " entries)")
	#normalization = histograms[i].GetEntries()
	#histograms[i].Scale(1./normalization)
	#histograms[i].GetYaxis().SetTitle("relative abundance")
	#histograms[i].SetLineColor(ROOT.kWhite + i)
	#histograms[i].SetLineColor(ROOT.kGray + i)
	#histograms[i].SetFillColor(ROOT.kGray + i)
	if 0==i:
		histograms[i].SetLineColor(ROOT.kGray)
		histograms[i].SetFillColor(ROOT.kGray)
#		histograms[0].Draw()
	elif 1==i:
		histograms[i].SetLineColor(ROOT.kBlue)
	else:
		histograms[i].SetLineColor(ROOT.kRed)
#		histograms[i].Draw("same")
	histogram_stack.Add(histograms[i])
	i = i + 1
canvas1 = ROOT.TCanvas('canvas1', 'mycanvas', 100, 50, 800, 600)
#canvas1.SetBatch(1)
canvas1.SetLogx()
#canvas1.SetLogy()
histogram_stack.Draw("nostack")
histogram_stack.GetXaxis().SetTitle("deposited energy [keV]")
histogram_stack.GetYaxis().SetTitle("number of events")
histogram_stack.GetXaxis().CenterTitle(1)
histogram_stack.GetYaxis().CenterTitle(1)
histogram_stack.GetXaxis().SetTitleOffset(1.3)
histogram_stack.GetYaxis().SetMaxDigits(3)
#canvas1.BuildLegend()
legend1.Draw()
canvas1.Modified()
canvas1.Update()

if len(sys.argv) < 2:
	import time
	time.sleep(1)
else:
	#raw_input("Press Enter to continue...")
	imagefile = ROOT.TImage.Create()
	imagefile.FromPad(canvas1)
	imagefile.WriteImage(png_filename)
	print "generated " + png_filename

