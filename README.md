This project is to simulate the expected flux of synchrotron radition (x-ray photons) and the energy deposited in a silicon strip sensor instrumented on the Low Energy Ring (LER) and the High Energy Ring (HER) at SuperKEKB.

![alt text](XRM-geometry.png?raw=true "XRM geometry")

The "exampleB1" code is modified from the example project of the same name that comes with geant4.

helpful notes:

to build and install geant4:
https://github.com/mzandrew/bin/blob/master/physics/make_geant4_and_visualization_friends.sh

to build a geant4 executable:

```
. /usr/local/share/Geant4/geant4make/geant4make.sh
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
./bulk_si_HER HER-N-bunches.mac > HER-bulk_si.log
./edge_on_HER HER-N-bunches.mac > HER-edge_on.log
./face_on_HER HER-N-bunches.mac > HER-face_on.log
read 2671699 lines from file HER-bulk_si
total_energy_incident 6524.29642445 MeV per bunch
total_energy_deposited 6499.16526734 MeV per bunch
total_energy_incident 1.04530798255e-09 J per bunch
total_energy_deposited 1.04128152552e-09 J per bunch
total_power_incident 0.531944165967 W
total_power_deposited 0.529895152321 W
read 2802602 lines from file HER-edge_on
total_energy_incident 1504.79012802 MeV per bunch
total_energy_deposited 1390.30807343 MeV per bunch
total_energy_incident 2.41094062952e-10 J per bunch
total_energy_deposited 2.22752007697e-10 J per bunch
total_power_incident 0.122689754961 W
total_power_deposited 0.113355712317 W
read 2867576 lines from file HER-face_on
total_energy_incident 567.97320967 MeV per bunch
total_energy_deposited 562.791373454 MeV per bunch
total_energy_incident 9.09993800581e-11 J per bunch
total_energy_deposited 9.01691580067e-11 J per bunch
total_power_incident 0.0463084470193 W
total_power_deposited 0.0458859573951 W
generated XRM.HER.png
./bulk_si_LER LER-N-bunches.mac > LER-bulk_si.log
./edge_on_LER LER-N-bunches.mac > LER-edge_on.log
./face_on_LER LER-N-bunches.mac > LER-face_on.log
read 2619147 lines from file LER-bulk_si
total_energy_incident 4104.33136828 MeV per bunch
total_energy_deposited 4099.48835191 MeV per bunch
total_energy_incident 6.57586667307e-10 J per bunch
total_energy_deposited 6.56810730204e-10 J per bunch
total_power_incident 0.334637635159 W
total_power_deposited 0.334242770466 W
read 2711466 lines from file LER-edge_on
total_energy_incident 798.21338691 MeV per bunch
total_energy_deposited 770.447401231 MeV per bunch
total_energy_incident 1.27887939301e-10 J per bunch
total_energy_deposited 1.23439336021e-10 J per bunch
total_power_incident 0.065080573711 W
total_power_deposited 0.0628167351093 W
read 2775469 lines from file LER-face_on
total_energy_incident 455.24275851 MeV per bunch
total_energy_deposited 453.445355438 MeV per bunch
total_energy_incident 7.29379627331e-11 J per bunch
total_energy_deposited 7.26499868877e-11 J per bunch
total_power_incident 0.0371172175104 W
total_power_deposited 0.0369706702023 W
generated XRM.LER.png
```

![alt text](XRM.HER.png?raw=true "XRM HER")

![alt text](XRM.LER.png?raw=true "XRM LER")

