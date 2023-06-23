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

## untar measurement set to working directory
mv split_channels.py /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/30Dor
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/30Dor

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p ${ms_file} -s ${start_chan} -e ${end_chan}

## loop through to tar each split out file
for ((i=$3; i<=$4; i++))
do
	tar -cvf ${ms_file}_chan${i}.tar ${ms_file}_chan${i}
	#mv ${ms_file}.contsub_chan${i}.tar /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}/30Dor
done

rm split_channels.py
