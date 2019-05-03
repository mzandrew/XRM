#!/bin/bash -e

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir

gvim exampleB1.cc *.mac edit.sh go.sh spectra.py src/* include/* 1>/dev/null 2>&1 &

