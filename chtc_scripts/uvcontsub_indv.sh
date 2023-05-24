#!/bin/bash
#
# uvcontsub_indv.sh
# execution script to apply continuum subtraction to 

mv uvcontsub_indv.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

##  set measurement set name, copy and untar
## untar measurement set
ms_name=$1"_shifted.tar"
tar -xvf /projects/vla-processing/GASKAP-HI/measurement_sets/38814/phase_shifted/$ms_name --directory .
untar_name=$1

## define channel list
chanRange="0 250 850 1400 1750 2111"
order=0

## make call to casa
casa-6.5.0-15-py3.8/bin/casa -c uvcontsub_indv.py -l $chanRange -o $order -n $untar_name

## pack up and copy back
tar -cvf $untar_name"_contsub.tar" $untar_name".contsub"

mv $untar_name"_contsub.tar" /projects/vla-processing/GASKAP-HI/measurement_sets/38814/contsub 
rm -rf $untar_name
