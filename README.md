to build a geant4 executable:
. /usr/local/share/Geant4-10.5.1/geant4make/geant4make.sh
mkdir build; cd build; cmake ..; make

to rebuild a geant4 executable after a source change:
(to run with a new .mac file, copy the changed mac file into the build dir first)
cd build; make

to run a geant4 executable (from build/ subdir):
. /usr/local/bin/geant4.sh
cd build; ./exampleB1

edge-on:
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log
mza@ubuntu18-04:~/build/XRM/build$ grep -c deposited *.log
HER.log:70
LER.log:133

face-on:
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log
mza@ubuntu18-04:~/build/XRM/build$ grep -c deposited *.log
HER.log:389
LER.log:228

