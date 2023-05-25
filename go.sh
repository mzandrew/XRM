#!/bin/bash -e

# written 2019-04-30 by mza
# last updated 2023-05-25 by mza

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

declare -i MAX_CPUS_TO_USE=16 # to limit the max # of CPU cores to use
declare -i    SHOULD_BUILD=1 # whether we should (re)build the simulations
declare -i SHOULD_GENERATE=1 # whether we should run the simulations
declare -i     SHOULD_PLOT=1 # whether we should produce the plots

#declare situation_list="bulk_si edge_on edge_on_CeYAG face_on"
#declare situation_list="bulk_si edge_on edge_on_scint edge_on_scint_gold"
#declare situation_list="edge_on edge_on_scint edge_on_scint_gold"
declare situation_list="edge_on_scint_gold"
declare -i NUMBER_OF_RUNS=2 # half HER, half LER
declare -x G4FORCENUMBEROFTHREADS=16

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# sudo apt install -y python3-dev cmake qtdeclarative5-dev libxm4
# cd /usr/lib/x86_64-linux-gnu
# sudo ln -s libXm.so.4 libXm.so
# sudo ln -s libSM.so.6 libSM.so
# sudo ln -s libICE.so.6 libICE.so
# sudo ln -s libXt.so.6 libXt.so
# sudo ln -s libXmu.so.6 libXmu.so
# sudo ln -s libXpm.so.4 libXpm.so
# sudo ln -s libexpat.so.1 libexpat.so

declare -i      FAKE_BUILD=0 # used to test this script
declare -i   FAKE_GENERATE=0 # used to test this script
declare -i       FAKE_PLOT=0 # used to test this script

declare -i NUMBER_OF_SITUATION_PER_RUN=0
for situation in $situation_list; do
	NUMBER_OF_SITUATION_PER_RUN=$((NUMBER_OF_SITUATION_PER_RUN+1))
done
#echo "NUMBER_OF_SITUATION_PER_RUN = $NUMBER_OF_SITUATION_PER_RUN"

declare -i TOTAL_NUMBER_OF_RUNS=$((NUMBER_OF_RUNS*NUMBER_OF_SITUATION_PER_RUN))
#echo "TOTAL_NUMBER_OF_RUNS = $TOTAL_NUMBER_OF_RUNS"
declare -i NUM_CPUS=$(grep -c "^processor" /proc/cpuinfo)
if [ $NUM_CPUS -gt $MAX_CPUS_TO_USE ]; then
	NUM_CPUS=$MAX_CPUS_TO_USE
fi
#echo "NUM_CPUS = $NUM_CPUS"
declare -i PARALLEL_GENERATE=0
if [ $TOTAL_NUMBER_OF_RUNS -lt $NUM_CPUS ]; then
	PARALLEL_GENERATE=1
	NUM_CPUS=$((NUM_CPUS/NUMBER_OF_RUNS))
else
	PARALLEL_GENERATE=0
fi
#echo "PARALLEL_GENERATE = $PARALLEL_GENERATE"
#echo "NUM_CPUS = $NUM_CPUS"

declare big_bpid_list=""
declare plot_bpid_list=""

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
if [ $SHOULD_BUILD -gt 0 ]; then
	if [ $FAKE_BUILD -eq 0 ]; then
		. /usr/local/share/Geant4/geant4make/geant4make.sh
		cmake ..
		make -j$NUM_CPUS
	fi
fi

if [ $SHOULD_GENERATE -gt 0 ]; then
	#echo "$ROOTSYS $PYTHONPATH"
	. /usr/local/bin/geant4.sh
	#echo "$ROOTSYS $PYTHONPATH"
fi

function wait_for_bpid_list_to_finish {
	local bpid_list="${@}"
	local -i bpid
	if [ ! -z "$bpid_list" ]; then
		echo -n "waiting for background processes $bpid_list ..."
		for bpid in $bpid_list; do
			wait $bpid
		done
		echo " done"
	fi
}

function do_ring {
	local HL="${1}"
	local -i N=0
	local bpid_list=""
	local string=""
	date
	if [ $SHOULD_GENERATE -gt 0 ]; then
		for situation in $situation_list; do
			if [ $PARALLEL_GENERATE -gt 0 ] || [ $N -lt $NUM_CPUS ]; then
				if [ $FAKE_GENERATE -eq 0 ]; then
					./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation} &
				else
					sleep 3 &
				fi
				string="./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation} [background pid $!]"
				echo "$string"; echo "$string" >/dev/stderr
				#echo "running ${situation}_${HL}ER in background as pid $!..."
				big_bpid_list="$big_bpid_list $!"
				bpid_list="$bpid_list $!"
				N=$((N+1))
			else
				string="./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}"
				echo "$string"; echo "$string" >/dev/stderr
				#echo "running ${situation}_${HL}ER..."
				if [ $FAKE_GENERATE -eq 0 ]; then
					./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}
				else
					sleep 3
				fi
				#echo "done with ${situation}_${HL}ER"
			fi
		done
		wait_for_bpid_list_to_finish $bpid_list
		date
	fi
	if [ $SHOULD_PLOT -gt 0 ]; then
		wait_for_bpid_list_to_finish $plot_bpid_list
		#. ${HOME}/build/root/bin/thisroot.sh
		. /usr/local/bin/thisroot.sh
		#echo "$ROOTSYS $PYTHONPATH"
		filename="XRM.${HL}ER.png"
		if [ $FAKE_PLOT -eq 0 ]; then
		#../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-face_on
		#../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-edge_on_scint ${HL}ER-edge_on_scint_gold
			string=""
			for situation in $situation_list; do
				string="$string ${HL}ER-${situation}"
			done
			#../spectra.py $filename ${HL}ER-edge_on ${HL}ER-edge_on_scint ${HL}ER-edge_on_scint_gold && mv $filename .. &
			#echo "$string"; echo "$string" >/dev/stderr
			../spectra.py $filename $string && mv $filename .. &
		else
			sleep 4 &
		fi
		string="generating plot [background pid $!]"
		echo "$string"; echo "$string" >/dev/stderr
		plot_bpid_list="$plot_bpid_list $!"
		big_bpid_list="$big_bpid_list $!"
	fi
	date
}

function pau {
	echo "caught ctrl-c"
	#wait_for_bpid_list_to_finish $big_bpid_list
	kill $big_bpid_list
	exit 1
}

trap pau SIGINT

if [ $PARALLEL_GENERATE -gt 0 ]; then
	echo "running HER simulation in background..."
	do_ring H >> output-HER.log &
	echo "running LER simulation..."
	do_ring L >> output-LER.log
	sleep 1
	wait_for_bpid_list_to_finish $plot_bpid_list
else
	echo "running HER simulation..."
	do_ring H >> output-HER.log
	echo "running LER simulation..."
	do_ring L >> output-LER.log
	sleep 1
	wait_for_bpid_list_to_finish $plot_bpid_list
fi

