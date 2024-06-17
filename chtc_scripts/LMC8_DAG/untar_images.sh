#!/bin/bash
#
# untar_images.sh
# execution script for untarring processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
sbid=$1
file_suffix=$2
root_file_name=$3
chan=$4
image_output_name=${root_file_name}_chan${chan}-${file_suffix}.im
beam_output_name=${root_file_name}_chan${chan}-beam.bm

## check if 0 needs to be appended in name (channel range from 0 to 9) for alphanumeric ordering
if [ "${chan}" -lt "10" ]; then
        image_output_name=${root_file_name}_chan000${chan}-${file_suffix}.fits
        beam_output_name=${root_file_name}_chan000${chan}-beam.fits
fi
## check if 0 needs to be appended in name (channel range from 10 to 99) for alphanumeric ordering
if [ "${chan}" -lt "100" ] && [ "${chan}" -gt "9" ]; then
        image_output_name=${root_file_name}_chan00${chan}-${file_suffix}.fits
        beam_output_name=${root_file_name}_chan00${chan}-beam.fits
fi
## check if 0 needs to be appended in name (channel range from 100 to 999) for alphanumeric ordering
if [ "${chan}" -lt "1000" ] && [ "${chan}" -gt "99" ]; then
        image_output_name=${root_file_name}_chan0${chan}-${file_suffix}.fits
        beam_output_name=${root_file_name}_chan0${chan}-beam.fits
fi

## untar
tar -xvf /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities/${root_file_name}_chan${chan}.tar --directory .

## move image and pb fits files to designated directory
mv ${root_file_name}_chan${chan}-${file_suffix}.fits /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities/${image_output_name}
mv ${root_file_name}_chan${chan}-beam.fits /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities/${beam_output_name}

## clean up
rm -rf ${root_file_name}_chan${chan}*