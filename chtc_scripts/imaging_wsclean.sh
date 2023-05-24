#!/bin/bash
#
# imaging_wsclean.sh
# execution script for imaging of single GASKAP survey

## directory containing channel measurement sets
data_dir="/projects/vla-processing/GASKAP-HI/measurement_sets/38814/contsub"

## untar channels
for tar_file in ${data_dir}"/"*"_chan"$1".tar"
do
	tar -xf ${tar_file} --directory .
done

## set imaging parameters
total_iters=40000
minor_thresh=0.015 ##Jy
m_gain=0.7
robust=0.75
imsize=4096 
cellsize="7asec"
compute_threads=4
beam_size=30 ## arcsec
multiscale_bias=0.85
num_major_limit=5
output_name="GASKAP_SB38814_chan"$1
mask_path=SB38814_deconvolve_mask.fits
config_path=beammap_SB38814.config

## call to imager
#/usr/local/openmpi/bin/mpirun wsclean-mp \
wsclean \
	-use-idg \
	-aterm-config ${config_path} \
	-field 0,1,2 \
	-name ${output_name} \
	-weight briggs ${robust} \
	-size ${imsize} ${imsize} \
	-scale ${cellsize} \
	-pol i \
	-verbose \
	-fits-mask ${mask_path} \
	-auto-mask 3 \
	-auto-threshold 0.3 \
	-save-first-residual \
	-taper-gaussian 14 \
	-nmiter ${num_major_limit} \
	-mgain 0.7 \
	-niter ${total_iters} \
	-threshold ${minor_thresh} \
	-multiscale-gain 0.1 \
	-multiscale -multiscale-scale-bias ${multiscale_bias} \
	-log-time \
	-j ${compute_threads} *"_chan"$1 | tee ${output_name}".log"

## tar result
tar -cvf ${output_name}".tar" ${output_name}*

mv ${output_name}".tar" /projects/vla-processing/GASKAP-HI

## clean up
rm -rf *"chan"$1
rm -rf $output_name*
