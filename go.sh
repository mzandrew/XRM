#!/bin/bash -e

cd build
make
cp ../*.mac .

./exampleB1 HER-N-bunches.mac | grep "^[0-9]" > HER.log
grep -cvH " 0.0$" HER.log || /bin/true
grep -v " 0.0$" HER.log | sort -n > HER.summary

./exampleB1 LER-N-bunches.mac | grep "^[0-9]" > LER.log
grep -cvH " 0.0$" LER.log || /bin/true
grep -v " 0.0$" LER.log | sort -n > LER.summary

cd ..
gnuplot spectrum.gnuplot

