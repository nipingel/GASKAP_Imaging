#!/bin/bash

## script to rsync the 36 measurement sets in an closepack36 interleave from ANU's Avatar server

## define interleave, SBID, Project name 
rootDir=/avatar/nipingel/ASKAP/SMC/data/pilot_obs/ms_data/
interVal=A
SBID_1=10941
SBID_2=10944
fieldName=GASKAP_M344-11B_T0-0

## define destination directory
destDir=/fred/oz145/data/pilot_obs/ms_data/altered/$SBID_1"_"$SBID_2/$fieldName$interVal/CONTSUB

## loop through and rsync each beam
for bm in {0..35}
do
	if [ $bm -lt 10 ]
	then
		bm='0'$bm
	fi 
	rsync -azP avatar:$rootDir/$SBID_1"_"$SBID_2/$fieldName$interVal/CONTSUB/scienceData_SB$SBID_1"_SB"$SBID_2"_"$fieldName$interVal.beam"$bm"_SL.binned.contsub $destDir
done
