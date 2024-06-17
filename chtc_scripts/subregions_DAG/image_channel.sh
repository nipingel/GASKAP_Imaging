#!/bin/bash
#
# imaging_wsclean.sh
# execution script for imaging of single GASKAP survey

## get user provided variables
sbid=$1
chan=$2 
config_file=$3
output_prefix=$4

## directory containing channel measurement sets
data_dir=/projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}

## untar channels
for tar_file in ${data_dir}/*_chan${chan}.tar
do
	tar -xf ${tar_file} --directory .
done

## set imaging parameters
total_iters=10000
minor_thresh=0.015 ##Jy
m_gain=0.7
robust=0.75
imsize=3000
cellsize="3.25asec"
compute_threads=4
beam_size=18 ## arcsec
multiscale_bias=0.85
num_major_limit=5
output_name=${output_prefix}_chan${chan}
config_path=${config_file}

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
	-beam-size ${beam_size} \
	-pol i \
	-verbose \
	-auto-mask 3 \
	-auto-threshold 0.3 \
	-save-first-residual \
	-nmiter ${num_major_limit} \
	-mgain 0.7 \
	-niter ${total_iters} \
	-threshold ${minor_thresh} \
	-multiscale-gain 0.1 \
	-multiscale -multiscale-scale-bias ${multiscale_bias} \
	-log-time \
	-j ${compute_threads} *_chan${chan} | tee ${output_name}.log

## tar result
tar -cvf ${output_name}.tar ${output_name}*

mv -f ${output_name}.tar /projects/vla-processing/GASKAP-HI/images/${sbid}

## clean up
rm -rf *chan${chan}
rm -rf ${output_name}*
