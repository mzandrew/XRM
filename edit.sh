#!/bin/bash -e

declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
cd $localdir

gvim exampleB1.cc *.mac edit.sh go.sh src/* include/* 2>/dev/null &

