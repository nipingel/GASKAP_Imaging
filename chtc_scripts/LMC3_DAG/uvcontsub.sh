#!/bin/bash
#
# uvcontsub_indv.sh
# execution script to apply continuum subtraction to GASKAP measurement sets

## change home directory so CASA will run
HOME=$PWD

##  set user variables
sbid=$1
ms_name=$2
chan_str=$3
order=0

## change to staging area 
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c uvcontsub.py -l ${chan_str} -o ${order} -n ${ms_name}