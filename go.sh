#!/bin/bash -e

declare -i build=1 generate=1 plot=1

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir
mkdir -p build
cd build
if [ $build -gt 0 ]; then
	. /usr/local/share/Geant4-10.5.1/geant4make/geant4make.sh
	cmake ..
	make -j2
fi

#echo "$ROOTSYS $PYTHONPATH"
. /usr/local/bin/geant4.sh
#echo "$ROOTSYS $PYTHONPATH"
. ${HOME}/build/root/bin/thisroot.sh
#echo "$ROOTSYS $PYTHONPATH"

for HL in H L; do
	if [ $generate -gt 0 ]; then
		for situation in bulk_si edge_on face_on; do
			echo "./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}"
			./${situation}_${HL}ER ${HL}ER-N-bunches.mac > ${HL}ER-${situation}
			#grep -cvH " 0.0$" ${HL}ER-${situation}.log || /bin/true
		done
	fi
	if [ $plot -gt 0 ]; then
		filename="XRM.${HL}ER.png"
		#../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on ${HL}ER-face_on
		../spectra.py $filename ${HL}ER-bulk_si ${HL}ER-edge_on
		mv $filename ..
	fi
done

