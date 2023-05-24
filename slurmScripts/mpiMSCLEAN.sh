#!/bin/bash
#SBATCH --job-name clean307
## resource allocation
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem-per-cpu=6000
#SBATCH --time=01-00:00:00

## email parameters
#SBATCH --mail-user=Nickolas.Pingel@anu.edu.au
#SBATCH --mail-type=ALL

## set up job array: one per 6 ms files
#SBATCH --array=0-27

cd /fred/oz145/pros/GASKAP_Imaging/casaConfigScripts/
job_num=$SLURM_ARRAY_TASK_ID 

## define channel range to image based on job array ID
chanNum=$((244 + $job_num))

## select which beams to include
startBeam=0
endBeam=35

## set the environment variable for the mpi launcher explicitly, otherwise it defaults to 1 to avoid over-subscription
#OMP_NUM_THREADS=$SLURM_NTASKS


## set beams/interleaves to skip. Each string in skipInterleave array contains 
## the interleaves to skip for the specified beam in skipBeams
skipBeams=37
skipInter=ABC

## set imaging parameters
totNiter=0
nCycleNiter=2000
minorThresh=10 ##mJy
subDir=CONTSUB
output=GASKAP_10941_10944_MSCLEAN_scale32_iter20000_bias0.4_CHAN$chanNum
phaseCenter="J2000 00h58m43s -72d31m49"

../../casa-pipeline-release-5.6.1-8.el7/bin/mpicasa -n 5 ../../casa-pipeline-release-5.6.1-8.el7/bin/casa --logfile $output".log" --nogui --log2term -c mpiMSCLEAN.py -t $totNiter -n $nCycleNiter -w $minorThresh -d $subDir -o $output -p="$phaseCenter" -s $startBeam -e $endBeam -b $skipBeams -i $skipInter -l $chanNum    
