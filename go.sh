#!/bin/bash -e

declare -i build=1 generate=1 plot=1
declare -i parallel_generate=1
declare -i num_cpus=$(grep -c "^processor" /proc/cpuinfo)

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
if [ $build -gt 0 ]; then
	. /usr/local/share/Geant4-10.7.1/geant4make/geant4make.sh
	cmake ..
	make -j$num_cpus
fi

#echo "$ROOTSYS $PYTHONPATH"
. /usr/local/bin/geant4.sh
#echo "$ROOTSYS $PYTHONPATH"
. ${HOME}/build/root/bin/thisroot.sh
#echo "$ROOTSYS $PYTHONPATH"

#declare situation_list="bulk_si edge_on edge_on_CeYAG face_on"
#declare situation_list="bulk_si edge_on edge_on_scint edge_on_scint_gold"
declare situation_list="edge_on edge_on_scint edge_on_scint_gold"
num_cpus=$((num_cpus/2)) # half HER, half LER

function do_ring {
	local HL="${1}"
	local -i N=0
	local bpid_list=""
	if [ $generate -gt 0 ]; then
		for situation in $situation_list; do
			echo "./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}"
			if [ $parallel_generate -gt 0 ] || [ $N -ge $num_cpus ]; then
				./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation} &
				bpid_list="$bpid_list $!"
				N=$((N+1))
			else
				./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}
			fi
		done
		if [ $parallel_generate -gt 0 ]; then
			for bpid in $bpid_list; do
				wait $bpid
			done
		fi
	fi
	if [ $plot -gt 0 ]; then
		filename="XRM.${HL}ER.png"
		#../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-face_on
		#../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-edge_on_scint ${HL}ER-edge_on_scint_gold
		../spectra.py $filename ${HL}ER-edge_on ${HL}ER-edge_on_scint ${HL}ER-edge_on_scint_gold
		mv $filename ..
	fi
}

if [ $parallel_generate -gt 0 ]; then
	echo "running HER simulation in background..."
	do_ring H >> output-HER.log &
	echo "running LER simulation..."
	do_ring L | tee -a output-LER.log
else
	echo "running HER simulation..."
	do_ring H | tee -a output-HER.log
	echo "running LER simulation..."
	do_ring L | tee -a output-LER.log
fi

