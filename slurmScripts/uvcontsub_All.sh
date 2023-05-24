#!/bin/bash
#SBATCH --job-name contSub
#SBATCH --output=contSubSummary
## resource allocation
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16000
#SBATCH --time=00-04:00:00

## email parameters
#SBATCH --mail-user=Nickolas.Pingel@anu.edu.au
#SBATCH --mail-type=ALL

## set up job array: one per 6 ms files (2 beams X 3 interleaves)
#SBATCH --array=0-17

## function to check if an input value to in an array
function containsBeams () {
        local compareVar=$1
        shift
        local bmArray=("$@")
        beamIn=1
        for bm in "${bmArray[@]}";
                do
                if [[ $bm -eq $compareVar ]];
                        then
                        beamIn=0
                        break
                fi
        done
        return $beamIn
}

## function to check if an input character is in string
function containsInters () {
        local compareInter=$1
        local interVals=$2
        interIn=1
        if [[ $interVals == *$compareInter* ]]; then
                interIn=0
        fi
        return $interIn
}

cd /fred/oz145/pros/GASKAP_Imaging/casaConfigScripts
job_num=$PBS_ARRAY_INDEX

## define path variables
subDir="BINNED"
fieldName="GASKAP_M344-11B_T0-0"
SBID_1="10941"
SBID_2="10944"

## set channel range
chanRange="0 140 300 340 400 500"
order=1

## set base path to data
baseDataPath="/fred/oz145/data/pilot_obs/ms_data"

## start processing of (beamsXinterleaves) 2x3=6 ms files on this cpu instance
startBeam=$(($job_num * 2))
endBeam=$(($startBeam + 2))

## set beams/interleaves to skip. Each string in skipInterleave array contains 
## the interleaves to skip for the specified beam in skipBeams
skipBeams=(37)
skipInter=(ABC)
skipCnt=0

## Loop through the starting and end beam. 
## Each iteration will call a single instance of CASA
## to run uvContSub_Indv.py with the specified channel string
## and polynomial fit order as inputs

for ((beamNum=$startBeam;beamNum<$endBeam;beamNum++));
	do
	## append '0' if beamNum is less than 10
        if [ $beamNum -lt 10 ];
        then
        	beamNum=$( printf '%02d' $beamNum )
        fi
        
	echo "Processing beam number "$beamNum

	for inter in A B C;
	do
		echo "Processing interleave "$inter

		## check if we need to skip this beam/interleave pair
		containsBeams $beamNum ${skipBeams[@]}
		## check if interleave needs to be skipped
		if [[ $beamIn -eq 0 ]]; then
			containsInters $inter ${skipInter[$skipCnt]}
			if [[ $interIn -eq 0 ]]; then 
				echo "Skipping beam "$beamNum"; interleave "$inter
				continue
			fi
		fi
		
		## define data paths
		dataPath=$baseDataPath"/"$SBID_1"_"$SBID_2"/"$fieldName$inter"/BINNED"
		msName=$dataPath"/scienceData_SB"$SBID_1"_SB"$SBID_2"_"$fieldName$inter".beam"$beamNum"_SL.binned"

		## make call to casa
		casa --logfile "contSubBeam"$beamNum"_inter"$inter".log" -c uvContSub_Indv.py -l $chanRange -o $order -n $msName
	done

	## incrememnt skipCnt if we skipped an interleave/beam pair 
	if [[ $beamIn -eq 0 ]]; then 
		((skipCnt++))
	fi

    ## remove leading zero for next iterations
    beamNum=${beamNum#0}
done




