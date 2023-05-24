#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

cd tmp

## use wget to download link
wget $1

## move to designated directory
mv scienceData* /projects/vla-processing/GASKAP-HI/measurement_sets/38814
