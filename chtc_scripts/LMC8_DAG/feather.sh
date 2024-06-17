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
beam_file=$4
sd_file_name=$5

## change working directory to staging area
mv feather.py /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities
cd /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities

casa -c feather.py -f ${file_name} -o ${output_name} -s ${sd_file_name} -b ${beam_file}

## clean up
rm feather.py
