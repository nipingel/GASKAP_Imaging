#!/bin/bash
#
# split_channels.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set 

## change home directory so CASA will run
HOME=$PWD

## untar measurement set to working directory
tar -xvf /projects/vla-processing/GASKAP-HI/measurement_sets/38814/contsub/$1"_contsub.tar" --directory .

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p $1".contsub" -s $2 -e $3

## loop through to tar each split out file
for ((i=$2; i<=$3; i++))
do
	tar -cvf $1".contsub_chan"$i".tar" $1".contsub_chan"$i
	mv $1".contsub_chan"$i".tar" /projects/vla-processing/GASKAP-HI/measurement_sets/38814/contsub/
done

## clean up
rm -rf $1".contsub"
rm -rf $1".contsub_chan"*

