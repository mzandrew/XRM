#!/bin/bash -e

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
cmake ..
make
#cp ../*.mac .

for HL in H L; do
	for situation in bulk_si edge_on face_on; do
		./${situation} ${HL}ER-N-bunches.mac | grep "^[0-9]" > ${HL}ER-${situation}.log
		grep -v " 0.0$" ${HL}ER-${situation}.log | sort -n > ${HL}ER-${situation}
		#grep -cvH " 0.0$" ${HL}ER-${situation}.log || /bin/true
	done
	filename="XRM.${HL}ER.png"
	../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-face_on
	mv $filename ..
done

cd ..
#gnuplot spectrum.gnuplot
#${HOME}/build/root/bin/thisroot.sh
#echo "eog build/*.png"

