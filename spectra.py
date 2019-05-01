#!/usr/bin/env python

import re # search
import ROOT # TH1F
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
			input_energies[event_number] = input_energy
			deposited_energies[event_number] = deposited_energy
	histograms.append(ROOT.TH1F('histogram['+str(i)+']', title, number_of_bins, fbin_widths))
	#for event in input_energies.keys():
	#	histograms[i].Fill(input_energies[event])
	for event in deposited_energies.keys():
		histograms[i].Fill(deposited_energies[event])
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

