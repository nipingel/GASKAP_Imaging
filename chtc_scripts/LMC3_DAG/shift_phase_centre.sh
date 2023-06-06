#!/bin/bash
#
# set_phase_centre.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

##  set measurement set nam, RA, and DEC strings
ms_name=$1
ra_str=$2
dec_str=$3

## change directory to where measurement sets are stored in staging area
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid} 

## change the phase centre
chgcentre ${ms_name} ${ra_str} ${dec_str}