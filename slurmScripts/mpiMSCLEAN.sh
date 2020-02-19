#
#### JOB NAME
#PBS -N clean525
### Ask for email at job start, end, and if aborted
###PBS -M Nickolas.Pingel@anu.edu.au
#PBS -M nicholas.killerby-smith@anu.edu.au
#PBS -m abe
#### Ask for 1 total nodes, 1 cores per one job instance
#PBS -l select=1:ncpus=4:mpiprocs=5:mem=8gb
#PBS -l place=scatter
#### Type of node: smallmem or largemem
#PBS -q largemem
#### job array: one job instance per velocity plane 
#PBS -J 0-27
cd /avatar/nipingel/ASKAP/SMC/pros/GASKAP_Imaging/casaConfigScripts
job_num=$PBS_ARRAY_INDEX

## define channel range to image based on job array ID
chanNum=$((400 + $job_num))
##chanNum=525

## select which beams to include
startBeam=0
endBeam=35

## set beams/interleaves to skip. Each string in skipInterleave array contains 
## the interleaves to skip for the specified beam in skipBeams
skipBeams=5
skipInter=ABC

## set imaging parameters
totNiter=36000
nCycleNiter=3000
minorThresh=5 ##mJy
subDir=CONTSUB
output=SMC_MSCLEAN_CHAN$chanNum
phaseCenter="J2000 00h52m44s -72d49m42"


## Inform user of explicit call to imager
../../casa-pipeline-release-5.6.2-2.el7/bin/mpicasa -n 5 ../../casa-pipeline-release-5.6.2-2.el7/bin/casa --logfile "tclean_Chan"$chanNum".log" -c mpiMSCLEAN.py -t $totNiter -n $nCycleNiter -w $minorThresh -d $subDir -o $output -p="$phaseCenter" -s $startBeam -e $endBeam -b $skipBeams -i $skipInter -l $chanNum
