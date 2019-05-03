#!/bin/bash -e

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
cmake ..
make
. /usr/local/bin/geant4.sh
. ${HOME}/build/root/bin/thisroot.sh

for HL in H L; do
	for situation in bulk_si edge_on face_on; do
		./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}.log
		grep -v " 0.0$" ${HL}ER-${situation}.log | grep "^[0-9]" | sort -n > ${HL}ER-${situation}
		#grep -cvH " 0.0$" ${HL}ER-${situation}.log || /bin/true
	done
	filename="XRM.${HL}ER.png"
	../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-face_on
	mv $filename ..
done

