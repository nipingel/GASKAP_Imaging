#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

cd tmp

## set source-specific parameters
file_name="GASKAP_SB38814_chan"$1
## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$2" -lt "10" ]; then
        output_name=$1"_chan00"$1
fi
if [ "$2" -lt "100" ] && [ "$2" -gt "9" ]; then
        output_name=$1"_chan0"$1
fi

## untar
tar -xvf /projects/vla-processing/GASKAP-HI/images/mw_velocties/${file_name}".tar" --directory .

## move to designated directory
GASKAP_SB38814_chan1600-beam.fits
mv *-image.fits /projects/vla-processing/GASKAP-HI/images/mw_velocities
mv *-beam.fits /projects/vla-processing/GASKAP-HI/images/mw_velocities

## clean up
rm -rf $file_name*

