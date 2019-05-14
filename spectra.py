#!/usr/bin/env python

# written 2019-04-30 by mza
# last updated 2019-05-13 by mza

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
	#print sys.argv[0] + sys.argv[1:]
	print " ".join(sys.argv[0:])
	sys.exit(1)
ROOT.gROOT.SetBatch(True)
import re # search
import math # log10
import numpy # float array

skim = 1
stop_short = False
number_of_bins = 200
low = 0.004
high = 70.
factor = 10.**(math.log10(high/low)/number_of_bins)
bin_widths = []
bin_widths.append(low)
for i in range(number_of_bins - 1):
	bin_widths.append(bin_widths[i]*factor)
bin_widths.append(high)
fbin_widths = numpy.array(bin_widths, dtype='float64')
epsilon_eV = 4.9
legend1 = ROOT.TLegend(0.15, 0.5, 0.5, 0.75)

J_per_eV = 1.60217733e-19
J_per_MeV = 1.0e6 * J_per_eV
bunches_per_second = 508.8875e6

total_energy_deposited_J = {}
total_power_deposited_W = {}
def show_energy_per_bunch_and_power(string):
	#print "total_energy_incident " + str(total_energy_incident_eV/1.e6) + " MeV per bunch"
	total_energy_incident_J = J_per_MeV * total_energy_incident_eV / 1.e6
	#print "total_energy_incident " + str(total_energy_incident_J) + " J per bunch"
	total_power_incident_W = total_energy_incident_J * bunches_per_second
	#print "total_power_incident %.3f W" % total_power_incident_W
	print "%.3f W incident" % (total_power_incident_W)
	for key in sorted(total_energy_deposited_eV, key=total_energy_deposited_eV.get, reverse=True):
		match = re.search(string, key)
		if match:
			#print "total_energy_deposited[" + key + "] " + str(total_energy_deposited_eV[key]/1.e6) + " MeV per bunch"
			total_energy_deposited_J[key] = J_per_MeV * total_energy_deposited_eV[key] / 1.e6
			#print "total_energy_deposited[" + key + "] " + str(total_energy_deposited_J[key]) + " J per bunch"
			total_power_deposited_W[key] = total_energy_deposited_J[key] * bunches_per_second
			#print "total_power_deposited[" + key + "] %.3f W" % total_power_deposited_W[key]
			print "%.3f W deposited in %s" % (total_power_deposited_W[key], key)

def parse_string(string):
#	print string
	match = re.search(" +([.e0-9-]+) ([:a-zA-Z0-9]+)(.*)$", string)
	if match:
		deposited_energy_eV = float(match.group(1))
		tag = match.group(2)
		remaining_string = match.group(3)
		not_done = len(remaining_string)
	return (deposited_energy_eV, tag, not_done, remaining_string)

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
histograms = {}
i = 0
title = " vs ".join(filenames)
histogram_stack = ROOT.THStack("histogram_stack", title)

for filename in filenames:
	print "reading file " + filename + "..."
	total_energy_incident_eV = 0.0
	total_energy_deposited_eV = {}
	histogram_initiated = 0
	#total_lines = sum(1 for line in open(filename))
	lines = 0
	matching_lines = 0
	for line in open(filename):
		lines = lines + 1
		if not 0==lines%skim:
			continue
		line = line.rstrip("\n\r")
		# evt# incident_E E1 process1 E2 process2 ... depE_a object_a depE_b object_b ...
		# 1 36.8176 13.63 phot 23.1876 eIoni 0 Air 0 BeFilter 36.8176 SiBulk
		match = re.search("^([0-9]+) +([.e0-9-]+)(.*)$", line)
		if match:
			matching_lines = matching_lines + 1
			event_number = int(match.group(1))
			incident_energy_eV = float(match.group(2))
			total_energy_incident_eV += incident_energy_eV
			remaining_string = match.group(3)
			not_done = len(remaining_string)
			while not_done:
				(deposited_energy_eV, tag, not_done, remaining_string) = parse_string(remaining_string)
				match = re.search("(phot|eIoni|msc|compt|eBrem|Rayl)", tag)
				if match:
					continue
				match = re.search("(HeBox)", tag)
				if match:
					continue
				if deposited_energy_eV < epsilon_eV:
					continue
				name = filename + "_" + tag
				match = re.search("bulk_si_Air", name)
				if match:
					continue
				match = re.search("bulk_si_BeFilter", name)
				if match:
					continue
				match = re.search("ER-face_on_(BeWindow|Air|BeFilter|CopperSlit)", name)
				if match:
					continue
				match = re.search("ER-edge_on_CeYAG_(BeWindow|Air|BeFilter|CopperSlit)", name)
				if match:
					continue
				try:
					total_energy_deposited_eV[name] += deposited_energy_eV
				except:
					total_energy_deposited_eV[name] = deposited_energy_eV
				try:
					histograms[name].Fill(deposited_energy_eV/1000.0)
				except:
					histograms[name] = ROOT.TH1F(name, title, number_of_bins, fbin_widths)
					histograms[name].Fill(deposited_energy_eV/1000.0)
			#print str(event_number) + " " + str(incident_energy) + " " + str(deposited_energy)
			if 0==matching_lines%100000:
				print "read " + str(matching_lines) + " lines from file " + filename + " so far..."
			if stop_short:
				if 300000==matching_lines:
					break
	print "read " + str(matching_lines) + " lines from file " + filename + " total"
	show_energy_per_bunch_and_power(filename)

	#normalization = histograms[i].GetEntries()
	#histograms[i].Scale(1./normalization)
	#histograms[i].GetYaxis().SetTitle("relative abundance")

j = 0
for key in sorted(total_power_deposited_W, key=total_power_deposited_W.get, reverse=True):
	histograms[key].SetLineColor(ROOT.kGreen + j)
	match = re.search("Be(Window|Filter)", key)
	if match:
		histograms[key].SetLineColor(ROOT.kCyan)
	match = re.search("Copper", key)
	if match:
		histograms[key].SetLineColor(ROOT.kOrange+1)
	match = re.search("SiBulk", key)
	if match:
		histograms[key].SetLineColor(ROOT.kGray)
		histograms[key].SetFillColor(ROOT.kGray)
	match = re.search("SiBeamDump", key)
	if match:
		histograms[key].SetLineColor(ROOT.kGray+1)
	match = re.search("Air", key)
	if match:
		histograms[key].SetLineColor(ROOT.kGray+2)
	match = re.search("SiEdgeOn", key)
	if match:
		histograms[key].SetLineColor(ROOT.kBlue)
	match = re.search("CeYAG_SiEdgeOn", key)
	if match:
		histograms[key].SetLineColor(ROOT.kMagenta)
#	match = re.search("SiFaceOn", key)
#	if match:
#		histograms[key].SetLineColor(ROOT.kRed)
	match = re.search("Ce:YAG", key)
	if match:
		histograms[key].SetLineColor(ROOT.kRed)
	histogram_stack.Add(histograms[key])
	legend1.AddEntry(histograms[key], "%.3f W %s (%d entries)" % (total_power_deposited_W[key], key, histograms[key].GetEntries()))
	j = j + 1

canvas1 = ROOT.TCanvas('canvas1', 'mycanvas', 100, 50, 1280, 1024)
canvas1.SetLogx()
canvas1.SetLogy()
histogram_stack.Draw("nostack")
histogram_stack.GetXaxis().SetTitle("deposited energy [keV]")
histogram_stack.GetYaxis().SetTitle("number of events")
histogram_stack.GetXaxis().CenterTitle(1)
histogram_stack.GetYaxis().CenterTitle(1)
histogram_stack.GetXaxis().SetTitleOffset(1.3)
histogram_stack.GetYaxis().SetMaxDigits(3)
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

