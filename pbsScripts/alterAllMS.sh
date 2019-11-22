#!/bin/bash

## 11/22/19

## After setting path variables, serially iterate over all ms files to call python script, fixPhaseCenters.py
## to apply beam offsets to default phase centers. Note that an ACES environment must be activated by typing '
## 'source initaces.sh', which is located in the misc directory. Perform in interactive job.

## set up directory structure such that the raw data have been copied to /altered/8906/FIELDNAME_INTERLEAVE 

##__author__ = "Nick Pingel"
##__version__ = "1.0"
##__email__ = "Nickolas.Pingel@anu.edu.au"
##__status__ = "Production"

dataDir='/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered/8906/'
fieldIDs=(SMC1-0_M344-11)
interLet=(A B C)
SBID=8906

## loop through each SBID, interleave and beam to provide fixPhaseCenter.py with name of MS
for s in {0..0}
do
	fieldID=${fieldIDs[s]}
	for i in {0..2}
	do
		inter=${interLet[i]}
		for bm in {0..35}
		do
			if [ $bm -lt 10 ]
			then 
				bm='0'$bm
			fi
			python ../utils/fixPhaseCenters.py -f $dataDir$fieldID$inter"/scienceData_SB"$SBID"_"$fieldID$inter".beam"$bm"_SL.ms"
		done
	done
done
