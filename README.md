to build a geant4 executable:
. /usr/local/share/Geant4-10.5.1/geant4make/geant4make.sh
mkdir build; cd build; cmake ..; make

to rebuild a geant4 executable after a source change:
(to run with a new .mac file, copy the changed mac file into the build dir first)
cd build; make

to run a geant4 executable (from build/ subdir):
. /usr/local/bin/geant4.sh
cd build; ./exampleB1

edge-on monochromatic 11 keV / 18 keV:
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log; grep -c deposited *.log
HER.log:70
LER.log:133

face-on monochromatic 11 keV / 18 keV:
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log; grep -c deposited *.log
HER.log:389
LER.log:228

bulk silicon cube for reference:
mza@ubuntu18-04:~/build/XRM$ ./go.sh
HER.log:8743
LER.log:21457

edge-on including InvSynFracInt with critial energy 7.18 keV / 4.458 keV:
mza@ubuntu18-04:~/build/XRM$ ./go.sh
HER.log:627
LER.log:723

face-on including InvSynFracInt with critial energy 7.18 keV / 4.458 keV:
mza@ubuntu18-04:~/build/XRM$ ./go.sh
HER.log:282
LER.log:381

