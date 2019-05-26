#!/bin/bash -e

mkdir -p pictures
declare filename="pictures/picture.jpg"
raspistill -rot 180 --nopreview --timeout 1 -o $filename

