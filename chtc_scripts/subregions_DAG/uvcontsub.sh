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
chan_str="0 300 800 1400 1750 2111"

## change to staging area 
mv uvcontsub.py /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/southern_ridge
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/southern_ridge

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa --log2term -c uvcontsub.py -l ${chan_str} -o ${order} -n ${ms_name}
rm uvcontsub.py
