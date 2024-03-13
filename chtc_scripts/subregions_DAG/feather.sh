#!/bin/bash
#
# feather.sh
# execution script to feather Parkes and ASKAP data

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
sbid=$1 
file_name=$2 
output_name=$3 
beam_cube_name=$4
sd_file_name=$5

## change working directory to staging area
mv feather.py /projects/vla-processing/GASKAP-HI/images/${sbid}
cd /projects/vla-processing/GASKAP-HI/images/${sbid}

/casa-6.5.0-15-py3.8/bin/casa -c feather.py -f ${file_name} -o ${output_name} -b ${beam_cube_name} -s ${sd_file_name}

## clean up
rm feather.py
