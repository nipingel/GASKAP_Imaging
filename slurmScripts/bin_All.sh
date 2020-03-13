#!/bin/bash
#SBATCH --job-name uvBin
#SBATCH --output=uvBinSummary
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

cd /fred/oz145/pros/GASKAP_Imaging/casaConfigScripts/
job_num=$PBS_ARRAY_INDEX

## define path variables
fieldName="SMC1-0_M344-11"
SBID="8906"

## set channel range
width=4

## set base path to data
baseDataPath="/fred/oz145/data/smc2019/msdata_smc/altered"

## start processing of (beamsXinterleaves) 2x3=6 ms files on this cpu instance
startBeam=$(($job_num * 2))
endBeam=$(($startBeam + 2))

## set beams/interleaves to skip. Each string in skipInterleave array contains 
## the interleaves to skip for the specified beam in skipBeams
skipBeams=(05)
skipInter=(ABC)
skipCnt=0

## Loop through the starting and end beam. 
## Each iteration will call a single instance of CASA
## to run bin_Indv.py with the specified channel width

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
		dataPath=$baseDataPath"/"$SBID$"/"$fieldName$inter
		msName=$dataPath"/scienceData_SB"$SBID"_"$fieldName$inter".beam"$beamNum"_SL.ms"

		## make call to casa
		casa --logfile "binBeam"$beamNum"_inter"$inter".log" -c bin_Indv.py -w $width -n $msName
	done

	## incrememnt skipCnt if we skipped an interleave/beam pair 
	if [[ $beamIn -eq 0 ]]; then 
		((skipCnt++))
	fi

	## remove leading zero for next iterations
	beamNum=${beamNum#0}
done




