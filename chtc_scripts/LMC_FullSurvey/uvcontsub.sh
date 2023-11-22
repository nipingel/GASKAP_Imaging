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
chan_str="0 250 850 1400 1750 2111"

## change to staging area 
cp -r /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/${ms_name} .

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c uvcontsub.py -l ${chan_str} -o ${order} -n ${ms_name}

## tar result
tar -cvf ${ms_name}.contsub.tar ${ms_name}.contsub
mv ${ms_name}.contsub /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}
