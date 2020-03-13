#!/bin/bash
#SBATCH --job-name clean_PB
#SBATCH --output=cleanSummary
## resource allocation
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=9
#SBATCH --mem-per-cpu=16000
#SBATCH --time=04-00:00:00

## email parameters
#SBATCH --mail-user=Nickolas.Pingel@anu.edu.au
#SBATCH --mail-type=ALL

## set up job array: one per 6 ms files
#SBATCH --array=0-27

cd /fred/oz145/pros/GASKAP_Imaging/casaConfigScripts/
job_num=$SLURM_ARRAY_TASK_ID 

## define channel range to image based on job array ID
chanNum=$((428 + $job_num))

## select which beams to include
startBeam=0
endBeam=35

## set beams/interleaves to skip. Each string in skipInterleave array contains 
## the interleaves to skip for the specified beam in skipBeams
skipBeams=5
skipInter=ABC

## set imaging parameters
totNiter=10000
nCycleNiter=2000
minorThresh=5 ##mJy
subDir=CONTSUB
output=SMC_MSCLEAN_scale64_iter10000_pbmask_CHAN$chanNum
phaseCenter="J2000 00h52m44s -72d49m42"

../../casa-pipeline-release-5.6.1-8.el7/bin/mpicasa -n 9 ../../casa-pipeline-release-5.6.1-8.el7/bin/casa --logfile $output".log" --nogui --log2term -c mpiMSCLEAN.py -t $totNiter -n $nCycleNiter -w $minorThresh -d $subDir -o $output -p="$phaseCenter" -s $startBeam -e $endBeam -b $skipBeams -i $skipInter -l $chanNum 
