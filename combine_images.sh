#!/bin/bash
#
# combine_images.sh
# execution script for combining processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
file_suffix=$1
src_name=$2
output_name=$3
delta_nu=$4

## change working directory to staging area
mv combine_images.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}


# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c combine_images.py -f ${file_suffix} -o ${output_name} -d ${delta_nu}

## clean up
rm combine_images.py