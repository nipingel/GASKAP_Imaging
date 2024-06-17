#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

## get user input
file_url=$1
sbid=$2

## transfer directly to staging area
mkdir -p /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}
cd /projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}

## use wget to download link
#wget -c --content-disposition $1
wget --content-disposition ${file_url}