#!/bin/bash
#
# set_phase_centre.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

##  set measurement set nam, RA, and DEC strings
ms_name=$1
sbid=$2
ra_str=$3
dec_str=$4

## change directory to where measurement sets are stored in staging area
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid} 

## change the phase centre
chgcentre ${ms_name} ${ra_str} ${dec_str}
