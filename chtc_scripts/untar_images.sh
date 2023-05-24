#!/bin/bash
#
# untar_images.sh
# execution script for untarring processed individual spectral channels

## unpack user arguments
file_suffix=$1
root_file_name=$2
sbid=$3
chan=$4
output_name=${root_file_name}_chan${chan}-${file_suffix}.fits

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "${chan}" -lt "10" ]; then
        output_name=${root_file_name}_chan00${chan}.${file_suffix}.fits
fi
## check if 0 needs to be appended in name (channel range from 100 to 999) for alphanumeric ordering
if [ "${chan}" -lt "100" ] && [ "${chan}" -gt "9" ]; then
        output_name=${root_file_name}_chan0${chan}.${file_suffix}.fits
fi

## untar
tar -xvf /projects/vla-processing/GASKAP-HI/images/${sbid}/mw_velocties/${root_file_name}_chan${chan}.tar --directory .

## move image and pb fits files to designated directory
mv ${root_file_name}_chan${chan}-${file_suffix}.fits /projects/vla-processing/GASKAP-HI/images/${sbid}/mw_velocities/${output_name}
mv ${root_file_name}_chan${chan}-beam.fits /projects/vla-processing/GASKAP-HI/images/${sbid}/mw_velocities/${output_name}

## clean up
rm -rf ${root_file_name}_chan${chan}*