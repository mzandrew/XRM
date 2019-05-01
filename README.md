This project is to simulate the expected flux of x-ray photons and the energy deposited in a silicon strip sensor instrumented on the Low Energy Ring (LER) and the High Energy Ring (HER) at SuperKEKB.

The "exampleB1" code is modified from the example project of the same name that comes with geant4.

helpful notes:

to build and install geant4:
https://github.com/mzandrew/bin/blob/master/physics/make_geant4_and_visualization_friends.sh

to build a geant4 executable:

```
. /usr/local/share/Geant4-10.5.1/geant4make/geant4make.sh
mkdir build; cd build; cmake ..; make
```

to rebuild a geant4 executable after a source change:
(to run with a new .mac file, copy the changed mac file into the build dir first)

```
cd build; make
```

to run a geant4 executable (from build/ subdir):

```
. /usr/local/bin/geant4.sh
cd build; ./edge_on
```

preliminary results:

edge-on monochromatic 11 keV / 18 keV:

```
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log; grep -c deposited *.log
HER.log:70
LER.log:133
```

face-on monochromatic 11 keV / 18 keV:

```
mza@ubuntu18-04:~/build/XRM/build$ cp ../*.mac .; ./exampleB1 HER-N-bunches.mac > HER.log ; ./exampleB1 LER-N-bunches.mac > LER.log; grep -c deposited *.log
HER.log:389
LER.log:228
```

bulk_si: bulk silicon cube in beampipe including SR spectrum (InvSynFracInt) with critial energy 7.18 keV / 4.458 keV

edge_on: including SR spectrum (InvSynFracInt) with critial energy 7.18 keV / 4.458 keV

face_on: including SR spectrum (InvSynFracInt) with critial energy 7.18 keV / 4.458 keV

```
mza@ubuntu18-04:~/build/XRM$ ./go.sh
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mza/build/XRM/build
[ 33%] Built target bulk_si
[ 66%] Built target face_on
[100%] Built target edge_on
read 8743 lines from file HER-bulk_si.summary
read 21457 lines from file LER-bulk_si.summary
read 627 lines from file HER-edge_on.summary
read 723 lines from file LER-edge_on.summary
read 282 lines from file HER-face_on.summary
read 381 lines from file LER-face_on.summary
```
