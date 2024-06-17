#!/bin/bash
#
# split_channels.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set 

## change home directory so CASA will run
HOME=$PWD

sbid=$1
ms_file=$2
start_chan=$3
end_chan=$4

cp -r /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/${ms_file}.contsub .

# make casa call to imaging script
casa -c split_channels.py -p ${ms_file}.contsub -s ${start_chan} -e ${end_chan}

## loop through to tar each split out file
for ((i=$3; i<=$4; i++))
do
	tar -cvf ${ms_file}.contsub_chan${i}.tar ${ms_file}.contsub_chan${i}
	mv ${ms_file}.contsub_chan${i}.tar /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}
done

## clean up
rm -rf ${ms_file}.contsub
