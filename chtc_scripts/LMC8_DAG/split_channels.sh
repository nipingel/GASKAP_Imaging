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

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p ${ms_file}.contsub -s ${start_chan} -e ${end_chan}

## loop through to tar each split out file
for ((i=$2; i<=$3; i++))
do
	tar -cvf ${ms_file}.contsub_chan${i}.tar ${ms_file}.contsub_chan${i}
	mv ${ms_file}.contsub_chan${i}.tar /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}
done

## clean up
rm -rf ${ms_file}.contsub
rm -rf ${ms_file}.contsub_chan*