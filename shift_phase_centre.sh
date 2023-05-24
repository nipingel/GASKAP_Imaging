#!/bin/bash
#
# set_phase_centre.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

cd tmp

##  set measurement set nam, copy and untar
tar_name=$1".tar"
cp /projects/vla-processing/GASKAP-HI/measurement_sets/38814/$tar_name .
tar -xvf $tar_name

## set phase centre string
phase_centre_str="04h32m25.1s -69d04m38s"

## change the phase centre
chgcentre $1 $phase_centre_str

## pack up and copy back
tar -cvf $1"_shifted.tar" $1
mv $1"_shifted.tar" /projects/vla-processing/GASKAP-HI/measurement_sets/38814/phase_shifted
rm $tar_name