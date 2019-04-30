#!/bin/bash -e

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
cmake ..
make
#cp ../*.mac .

for situation in bulk_si edge_on face_on; do
	for HL in H L; do
		./${situation} ${HL}ER-N-bunches.mac | grep "^[0-9]" > ${HL}ER-${situation}.log
		grep -v " 0.0$" ${HL}ER-${situation}.log | sort -n > ${HL}ER-${situation}.summary
		#grep -cvH " 0.0$" ${HL}ER-${situation}.log || /bin/true
		../spectra.py ${HL}ER-${situation}.summary
	done
done

cd ..
#gnuplot spectrum.gnuplot
#${HOME}/build/root/bin/thisroot.sh

