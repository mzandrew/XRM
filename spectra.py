#!/usr/bin/env python

#import os # path
#import sys # path
#sys.path.append(ps.path.join(os.path.expanduser("~"), "/build/root/lib"))
import ROOT # TH1F
import re # search
import math # log10
import numpy # float array

# written 2019-04-30 by mza
# last updated 2019-05-01 by mza

number_of_bins = 100
low = 0.004
high = 40.
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
	print "total_energy_incident " + str(total_energy_incident_keV/1000.0) + " MeV per bunch"
	print "total_energy_deposited " + str(total_energy_deposited_keV/1000.0) + " MeV per bunch"
	total_energy_incident_J = J_per_MeV * total_energy_incident_keV / 1000.0
	total_energy_deposited_J = J_per_MeV * total_energy_deposited_keV / 1000.0
	print "total_energy_incident " + str(total_energy_incident_J) + " J per bunch"
	print "total_energy_deposited " + str(total_energy_deposited_J) + " J per bunch"
	total_power_incident_W = total_energy_incident_J * bunches_per_second
	total_power_deposited_W = total_energy_deposited_J * bunches_per_second
	print "total_power_incident " + str(total_power_incident_W) + " W"
	print "total_power_deposited " + str(total_power_deposited_W) + " W"

legend1 = ROOT.TLegend(0.1, 0.7, 0.45, 0.9)
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
for filename in filenames:
	#print filename
	lines = []
	for line in open(filename):
		line = line.rstrip("\n\r")
		lines.append(line)
	print "read " + str(len(lines)) + " lines from file " + filename
	input_energies_keV = {}
	deposited_energies_keV = {}
	total_energy_incident_keV = 0.0
	total_energy_deposited_keV = 0.0
	for line in lines:
		match = re.search("^([0-9]+) +([.e0-9-]+) +([.e0-9-]+)$", line)
		if match:
			#print line
			event_number = int(match.group(1))
			input_energy_keV = float(match.group(2))
			deposited_energy_keV = float(match.group(3))
			total_energy_incident_keV += input_energy_keV
			total_energy_deposited_keV += deposited_energy_keV
			#print str(event_number) + " " + str(input_energy) + " " + str(deposited_energy)
			input_energies_keV[event_number] = input_energy_keV
			deposited_energies_keV[event_number] = deposited_energy_keV
	show_energy_per_bunch_and_power()
	histograms.append(ROOT.TH1F('histogram['+str(i)+']', title, number_of_bins, fbin_widths))
	#for event in input_energies.keys():
	#	histograms[i].Fill(input_energies[event])
	for event in deposited_energies_keV.keys():
		histograms[i].Fill(deposited_energies_keV[event])
	legend1.AddEntry(histograms[i], filename + " (" + str(int(histograms[i].GetEntries())) + " entries)")
	#normalization = histograms[i].GetEntries()
	#histograms[i].Scale(1./normalization)
	#histograms[i].GetYaxis().SetTitle("relative abundance")
	#histograms[i].SetLineColor(ROOT.kWhite + i)
	histograms[i].SetLineColor(ROOT.kGray + i)
	histograms[i].SetFillColor(ROOT.kGray + i)
#	if 0==i:
#		histograms[0].Draw()
#	else:
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
#canvas1.BuildLegend()
legend1.Draw()
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

