#!/usr/bin/env python3

# written 2019-04-30 by mza
# last updated 2023-05-26 by mza

import os # path, environ
import sys # path, exit, argv
#sys.path.append(ps.path.join(os.path.expanduser("~"), "/build/root/lib"))
try:
	import ROOT # TH1F
except:
	print("ROOT environment not setup yet")
	HOME = os.environ['HOME']
	#print(". " + HOME + "/build/root/bin/thisroot.sh; " + str(sys.argv))
	#print(". " + HOME + "/build/root/bin/thisroot.sh")
	print(". " + "/usr/local/bin/thisroot.sh")
	#print(sys.argv[0] + sys.argv[1:])
	print(" ".join(sys.argv[0:]))
	sys.exit(1)
ROOT.gROOT.SetBatch(True)
import re # search
import math # log10
import numpy # float array - sudo apt install -y python3-numpy

#mode = 1 # show everything by original name
#mode = 2 # executive summary: incoming, deposited
mode = 3 # incoming, upstream, scintillator, deposited, downstream
skim = 1
STOP_SHORT_CONSTANT = 300000
stop_short = False # just do the first STOP_SHORT_CONSTANT entries
number_of_bins = 100
low = 0.1
high = 100.
factor = 10.**(math.log10(high/low)/number_of_bins)
bin_widths = []
bin_widths.append(low)
for i in range(number_of_bins - 1):
	bin_widths.append(bin_widths[i]*factor)
bin_widths.append(high)
fbin_widths = numpy.array(bin_widths, dtype='float64')
epsilon1_eV = 4.9 # for total_energy_deposited_eV
epsilon2_eV = 99.9 # for histograms
legend1 = ROOT.TLegend(0.11, 0.6, 0.57, 0.8)
plot_epsilon_W = 0.001 # this is a comparison *after* scaling to the full beam power

J_per_eV = 1.60217733e-19
J_per_MeV = 1.0e6 * J_per_eV
bunches_per_second = 508.8875e6

def parse_string(string):
#	print(string)
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

match = re.search("HER", png_filename)
if match:
	power_ratio = 40.36 # HER
	title = "HER"
else:
	power_ratio = 21.48 # LER
	title = "LER"
power_ratio *= skim

histogram_stack = ROOT.THStack("histogram_stack", title)

total_energy_deposited_J = {}
total_power_deposited_W = {}
def determine_and_show_energy_per_bunch_and_power():
	#print("total_energy_incoming " + str(total_energy_incoming_eV/1.e6) + " MeV per bunch")
	#total_energy_incoming_J = J_per_MeV * total_energy_incoming_eV / 1.e6
	#print("total_energy_incoming " + str(total_energy_incoming_J) + " J per bunch")
	#total_power_incoming_W = total_energy_incoming_J * bunches_per_second
	#print("total_power_incoming %.3f W" % total_power_incoming_W)
	#print("%.3f W incoming" % (total_power_incoming_W))
	for key in sorted(total_energy_deposited_eV, key=total_energy_deposited_eV.get, reverse=True):
#		match = re.search(string, key)
#		if match:
		#print("total_energy_deposited[" + key + "] " + str(total_energy_deposited_eV[key]/1.e6) + " MeV per bunch")
		total_energy_deposited_J[key] = J_per_MeV * total_energy_deposited_eV[key] / 1.e6
		#print("total_energy_deposited[" + key + "] " + str(total_energy_deposited_J[key]) + " J per bunch")
		total_power_deposited_W[key] = total_energy_deposited_J[key] * bunches_per_second
		#print("total_power_deposited[" + key + "] %.3f W" % total_power_deposited_W[key])
		match = re.search("incoming", key)
		if match:
			print("%.3f W %s" % (power_ratio*total_power_deposited_W[key], key))
		else:
			#print("%.3f W deposited in %s" % (power_ratio*total_power_deposited_W[key], key))
			print("%.3f W %s" % (power_ratio*total_power_deposited_W[key], key))

for filename in filenames:
	print("reading file " + filename + "...")
	#total_energy_incoming_eV = 0.0
	total_energy_deposited_eV = {}
	histogram_initiated = 0
	#total_lines = sum(1 for line in open(filename))
	lines = 0
	matching_lines = 0
	#incoming = filename + "_incoming"
	incoming = "incoming"
	total_energy_deposited_eV[incoming] = 0.
	histograms[incoming] = ROOT.TH1F(incoming, title, number_of_bins, fbin_widths)
	for line in open(filename):
		lines = lines + 1
		if not 0==lines%skim:
			continue
		line = line.rstrip("\n\r")
		for thread_id in range(0,32):
			line = line.replace("G4WT" + str(thread_id) + " > ", "")
		# evt# incoming_E E1 process1 E2 process2 ... depE_a object_a depE_b object_b ...
		# 1 36.8176 13.63 phot 23.1876 eIoni 0 Air 0 BeFilter 36.8176 SiBulk
		match = re.search("^([0-9]+) +([.e0-9-]+)(.*)$", line)
		if match:
			matching_lines = matching_lines + 1
			event_number = int(match.group(1))
			try:
				incoming_energy_eV = float(match.group(2))
			except Exception as message:
				print("exception: " + str(message) + " while processing file " + filename + " line " + str(lines))
				continue
			histograms[incoming].Fill(incoming_energy_eV/1000.0)
			#total_energy_incoming_eV += incoming_energy_eV
			total_energy_deposited_eV[incoming] += incoming_energy_eV
			remaining_string = match.group(3)
			not_done = len(remaining_string)
			while not_done:
				handled = False
				(deposited_energy_eV, tag, not_done, remaining_string) = parse_string(remaining_string)
				name = tag
				match = re.search("(phot|eIoni|msc|compt|eBrem|Rayl)", tag)
				if match:
					handled = True
					continue
				if not handled:
					match = re.search("(SiBulk|HeBox)", tag)
					if match:
						handled = True
						if 2==mode:
							continue
						elif 3==mode:
							name = "other"
				if not handled:
					match = re.search("Air", tag)
					if match:
						handled = True
						if 2==mode:
							continue
						elif 3==mode:
							name = "other"
				if not handled:
					match = re.search("World", tag)
					if match:
						handled = True
						if 2==mode:
							name = "world"
							continue
						elif 3==mode:
							name = "other"
#				if not handled:
#					match = re.search("(BeFilter|BeWindow|DiamondMask|GoldMask|LuAG:Ce|Ce:YAG)", tag)
#					if match:
#						handled = True
#						if 2==mode: # executive summary of signal:no signal
#							continue
#						elif 3==mode:
#							name = "upstream"
				fullname = filename + "_" + tag
#				if not handled:
#					match = re.search("bulk_si_(BeFilter|BeWindow|DiamondMask|GoldMask|LuAG:Ce|Ce:YAG)", fullname)
#					if match:
#						handled = True
#						if 2==mode: # executive summary of signal:no signal
#							continue
#						elif 3==mode:
#							name = "upstream"
#				if not handled:
#					match = re.search("ER-edge_on_scint_(BeFilter|BeWindow|DiamondMask|GoldMask|SiBeamDump|LuAG:Ce|Ce:YAG)", fullname)
#					if match:
#						handled = True
#						if 2==mode: # executive summary of signal:no signal
#							continue
#						elif 3==mode:
#							name = "upstream"
				if not handled:
					match = re.search("ER-edge_on_scint_gold_(BeFilter|BeWindow|DiamondMask|GoldMask)", fullname)
					if match:
						handled = True
						if 2==mode: # executive summary of signal:no signal
							continue
						elif 3==mode:
							name = "upstream"
				if not handled:
					match = re.search("LuAG:Ce|Ce:YAG", tag)
					if match:
						handled = True
						if 2==mode: # executive summary of signal:no signal
							continue
						elif 3==mode:
							name = "scintillator"
#				if not handled:
#					match = re.search("(BeFilter|BeWindow|scint_gold_GoldMask|DiamondMask|SiBeamDump|LuAG:Ce|Ce:YAG)", fullname)
#					if match:
#						handled = True
#						if 2==mode: # executive summary of signal:no signal
#							continue
#						elif 3==mode:
#							name = "upstream"
				if not handled:
					match = re.search("(SiBeamDump)", tag)
					if match:
						handled = True
						if 2==mode: # executive summary of signal:no signal
							continue
						elif 3==mode:
							name = "downstream"
				#match = re.search("(BeFilter|BeWindow|scint_gold_GoldMask|DiamondMask|LuAG:Ce|Copper|SiBeamDump)", tag)
				#name = filename + "_SiEdgeOn_CopperBlock_SiHandle_WireBonds_Plating"
				if not handled:
					match = re.search("(CopperSlit|CopperBlock|SiHandle|WireBonds|Plating)", tag)
					if match:
						handled = True
						name = "apparatus"
				if not handled:
					match = re.search("(SiEdgeOn|InGaAsEdgeOn)", tag)
					if match:
						handled = True
						name = "sensor"
				if not handled:
					print("unhandled case: " + tag)
				if handled:
					if epsilon1_eV < deposited_energy_eV:
						try:
							total_energy_deposited_eV[name] += deposited_energy_eV
						except:
							total_energy_deposited_eV[name] = deposited_energy_eV
#					else:
#						print("ignoring " + str(deposited_energy_eV) + " eV")
					if epsilon2_eV < deposited_energy_eV:
						try:
							histograms[name].Fill(deposited_energy_eV/1000.0)
						except:
							histograms[name] = ROOT.TH1F(name, title, number_of_bins, fbin_widths)
							histograms[name].Fill(deposited_energy_eV/1000.0)
			#print(str(event_number) + " " + str(incoming_energy) + " " + str(deposited_energy))
			if 0==matching_lines%1000000:
				print("read " + str(matching_lines) + " lines from file " + filename + " so far...")
				sys.stdout.flush()
			if stop_short:
				if STOP_SHORT_CONSTANT==matching_lines:
					break
	print("read " + str(matching_lines) + " lines from file " + filename + " total")
	sys.stdout.flush()
	determine_and_show_energy_per_bunch_and_power()

	#normalization = histograms[i].GetEntries()
	#histograms[i].Scale(1./normalization)
	#histograms[i].GetYaxis().SetTitle("relative abundance")

for key in sorted(total_power_deposited_W, key=total_power_deposited_W.get):
	histograms[key].Scale(power_ratio)
	total_power_deposited_W[key] *= power_ratio

#for key in sorted(total_power_deposited_W, key=total_power_deposited_W.get):
#	print(key + " " + str(total_power_deposited_W[key]))

j = 0
histogram_stack_entries = 0
counter = {}
counter["Copper"] = 0
for key in sorted(total_power_deposited_W, key=total_power_deposited_W.get, reverse=True):
	should_plot = 1
	if total_power_deposited_W[key] < plot_epsilon_W:
		should_plot = 0
	j_should_increment = 1
	histograms[key].SetLineColor(ROOT.kCyan+j)
	histograms[key].SetLineWidth(4)
	match = re.search("(SiBulk|incoming)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kGray)
		histograms[key].SetFillColor(ROOT.kGray)
	match = re.search("(BeFilter)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kCyan)
	match = re.search("(BeWindow)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kCyan+2)
	match = re.search("(GoldMask|WireBonds)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kYellow)
	match = re.search("(DiamondMask|upstream)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kBlack)
	match = re.search("(Air)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kGray+2)
	match = re.search("(Copper)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kOrange+10-counter["Copper"])
		counter["Copper"] = counter["Copper"] + 1
	match = re.search("(LuAG:Ce|Ce:YAG|scintillator)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kRed)
	match = re.search("(SiHandle|apparatus)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kBlue+2)
	match = re.search("(SiEdgeOn|sensor)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kMagenta)
		should_plot = 1
#	match = re.search("SiFaceOn", key)
#	if match:
#		histograms[key].SetLineColor(ROOT.kRed)
	match = re.search("(SiBeamDump|downstream)", key)
	if match:
		j_should_increment = 0
		histograms[key].SetLineColor(ROOT.kGray+1)
#	match = re.search("(scint|scint_gold)_incoming", key)
#	if match:
#		should_plot = 0
	if should_plot:
		print("adding entry")
		histogram_stack_entries += 1
		histogram_stack.Add(histograms[key])
		#legend1.AddEntry(histograms[key], "%.3f W %s (%d entries)" % (total_power_deposited_W[key], key, histograms[key].GetEntries()))
		legend1.AddEntry(histograms[key], "%.3f W %s" % (total_power_deposited_W[key], key))
	if j_should_increment:
		j = j + 1
print(str(histogram_stack_entries) + " histograms")

if histogram_stack_entries:
	#canvas1 = ROOT.TCanvas('canvas1', 'mycanvas', 100, 50, 600, 400)
	canvas1 = ROOT.TCanvas('canvas1', 'mycanvas', 100, 50, 1920, 1080)
	canvas1.SetLogx()
	canvas1.SetLogy()
	histogram_stack.Draw("nostack,hist")
	histogram_stack.GetXaxis().SetTitle("energy [keV]")
	histogram_stack.GetYaxis().SetTitle("number of events")
	histogram_stack.GetXaxis().CenterTitle(1)
	histogram_stack.GetYaxis().CenterTitle(1)
	histogram_stack.GetXaxis().SetTitleOffset(1.3)
	histogram_stack.GetYaxis().SetMaxDigits(3)
	#gStyle->SetTitleFontSize(1.0)
	legend1.Draw()
	legend1.SetTextSize(0.04)
	histogram_stack.GetXaxis().SetLabelSize(0.05)
	histogram_stack.GetYaxis().SetLabelSize(0.05)
	histogram_stack.GetXaxis().SetTitleSize(0.05)
	histogram_stack.GetYaxis().SetTitleSize(0.05)
	histogram_stack.GetXaxis().SetTitleOffset(0.9)
	histogram_stack.GetYaxis().SetTitleOffset(0.9)
	canvas1.Modified()
	canvas1.Update()

if len(sys.argv) < 2:
	import time
	time.sleep(1)
else:
	#raw_input("Press Enter to continue...")
	if histogram_stack_entries:
		imagefile = ROOT.TImage.Create()
		imagefile.FromPad(canvas1)
		imagefile.WriteImage(png_filename)
		print("generated " + png_filename)

