#!/bin/bash
#
# combine_images.sh
# execution script for combining processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
sbid=$1 
file_suffix=$2 
output_name=$3 
delta_nu=$4
process_num=$5
beam_suffix="bm"

## change working directory to staging area
mv combine_images.py /projects/vla-processing/GASKAP-HI/images/${sbid}/mw_velocities
cd /projects/vla-processing/GASKAP-HI/images/${sbid}/mw_velocities

## decide which casa call to make (beam pattern cube or image cube)
## beam pattern
if [ ${process_num} -eq "0" ]; then
	/casa-6.5.0-15-py3.8/bin/casa -c combine_images.py -f ${beam_suffix} -o ${output_name}_beam -d ${delta_nu} --beam
fi
## image
if [ ${process_num} -eq "1" ]; then
	/casa-6.5.0-15-py3.8/bin/casa -c combine_images.py -f ${file_suffix} -o ${output_name} -d ${delta_nu} --image
fi
