#!/bin/bash
#
# image_channel_clean_mask.sh
# execution script for imaging of single channel in GASKAP survey
# to generate clean mask 

## get python distribution
wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh -O ~/anaconda.sh
bash ~/anaconda.sh -b -p $HOME/anaconda3
~/anaconda3/bin/conda clean -all -y  

export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

## create conda env for astro tools
~/anaconda3/bin/conda create -c conda-forge -y -n astro_env astropy pip numpy scipy matplotlib pip

source ~/anaconda3/etc/profile.d/conda.sh
conda activate astro_env

## get user provided variables
sbid=$1
chan=$2 
config_file=$3
output_name=$4

## directory containing channel measurement sets
data_dir=/projects/vla-processing/GASKAP-HI/measurement_sets/${sbid}

## untar channels
for tar_file in ${data_dir}/*_chan${chan}.tar
do
	tar -xf ${tar_file} --directory .
done

## set imaging parameters
total_iters=100
minor_thresh=0.015 ##Jy
m_gain=0.7
robust=0.75
#imsize=4096
imsize=4916
cellsize="7asec"
compute_threads=4
beam_size=30 ## arcsec
multiscale_bias=0.85
num_major_limit=5
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
	-pol i \
	-verbose \
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
	-j ${compute_threads} *"_chan"${chan} | tee ${output_name}".log"

## run trailing python script to generate clean mask
python generate_clean_mask.py -n {output_name}-beam.fits -o ${output_name} -t 0.3

## clean up
rm -rf *chan${chan}
mv ${output_name}* /projects/vla-processing/GASKAP-HI/images/${sbid}/magellanic_velocities
