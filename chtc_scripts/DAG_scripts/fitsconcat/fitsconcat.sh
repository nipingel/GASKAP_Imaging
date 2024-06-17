#!/bin/bash
#
# fitsconcat.sh
# execution script for combining processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
sbid=$1 
file_suffix=$2 
output_name=$3 
process_num=$4
beam_suffix="beam"

## change working directory to staging area
mv fitsconcat.py /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities
cd /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities

## decide which casa call to make (beam pattern cube or image cube)
## beam pattern
if [ ${process_num} -eq "0" ]; then
	python fitsconcat.py -p . -e ${beam_suffix} -o ${output_name}
fi
## image
if [ ${process_num} -eq "1" ]; then
	python fitsconcat.py -p . -e ${file_suffix} -o ${output_name}
fi