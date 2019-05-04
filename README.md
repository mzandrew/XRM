This project is to simulate the expected flux of synchrotron radition (x-ray photons) and the energy deposited in a silicon strip sensor instrumented on the Low Energy Ring (LER) and the High Energy Ring (HER) at SuperKEKB.

![alt text](XRM-geometry.png?raw=true "XRM geometry")

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

to run 100 events in the visualization:
```
/run/beamOn 100
```

to run a pyroot program:

```
. ${HOME}/build/root/bin/thisroot.sh
./spectra.py blah.png inputfile1 inputfile2
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
mza@ubuntu18-04:~/build/XRM$ time ./go.sh 
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mza/build/XRM/build
[ 16%] Built target edge_on_HER
[ 33%] Built target bulk_si_HER
[ 50%] Built target face_on_HER
[ 66%] Built target bulk_si_LER
[ 83%] Built target edge_on_LER
[100%] Built target face_on_LER
read 2396552 lines from file HER-bulk_si
total_energy_incident 5850.34435035 MeV per bunch
total_energy_deposited 5824.15868615 MeV per bunch
total_energy_incident 9.37328909082e-10 J per bunch
total_energy_deposited 9.33133501327e-10 J per bunch
total_power_incident 0.47699496522 W
total_power_deposited 0.474859974657 W
read 128371 lines from file HER-edge_on
total_energy_incident 1476.95432533 MeV per bunch
total_energy_deposited 1363.95464558 MeV per bunch
total_energy_incident 2.36634273749e-10 J per bunch
total_energy_deposited 2.18529721229e-10 J per bunch
total_power_incident 0.120420223982 W
total_power_deposited 0.111207043512 W
read 89164 lines from file HER-face_on
total_energy_incident 774.31649203 MeV per bunch
total_energy_deposited 767.723974367 MeV per bunch
total_energy_incident 1.24059232978e-10 J per bunch
total_energy_deposited 1.23002994743e-10 J per bunch
total_power_incident 0.0631321929219 W
total_power_deposited 0.0625946864872 W
generated XRM.HER.png
read 6184428 lines from file LER-bulk_si
total_energy_incident 9699.35538419 MeV per bunch
total_energy_deposited 9687.73242506 MeV per bunch
total_energy_incident 1.55400873122e-09 J per bunch
total_energy_deposited 1.55214652705e-09 J per bunch
total_power_incident 0.790815618206 W
total_power_deposited 0.789867965786 W
read 252243 lines from file LER-edge_on
total_energy_incident 2184.02109783 MeV per bunch
total_energy_deposited 2108.94106555 MeV per bunch
total_energy_incident 3.49918909118e-10 J per bunch
total_energy_deposited 3.37889756553e-10 J per bunch
total_power_incident 0.178069358864 W
total_power_deposited 0.171947873488 W
read 247267 lines from file LER-face_on
total_energy_incident 1745.83327374 MeV per bunch
total_energy_deposited 1739.30969343 MeV per bunch
total_energy_incident 2.79713449315e-10 J per bunch
total_energy_deposited 2.78668256067e-10 J per bunch
total_power_incident 0.142342677938 W
total_power_deposited 0.141810792159 W
generated XRM.LER.png
```

![alt text](XRM.HER.png?raw=true "XRM HER")

![alt text](XRM.LER.png?raw=true "XRM LER")

