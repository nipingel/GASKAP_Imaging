#!/bin/bash
#
# untar_measurement_sets.sh
# execution script to untar input measurement set 

sbid=$1
file_name=$2

cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/southern_ridge 

## untar 
tar -xvf ${file_name}
