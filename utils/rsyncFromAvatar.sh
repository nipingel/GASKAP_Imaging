#!/bin/bash

## script to rsync the 36 measurement sets in an closepack36 interleave from ANU's Avatar server

## define interleave, SBID, Project name 
rootDir=/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered
interVal=A
SBID=8906
objectName=SMC1-0_M344-11

## define destination directory
destDir=/fred/oz145/data/smc2019/msdata_smc/altered/$SBID/$objectName$interVal/CONTSUB

## loop through and rsync each beam
for i in {0..0}
do 
 #rsync -azP avatar:$rootDir/$SBID/$objectName$interVal/CONTSUB/scienceData_SB$SBID_$objectName$interVal.beam$i_SL.binned.contsub.tar
 rsync -azP avatar:$rootDir/$SBID/$objectName$interVal/CONTSUB/test.tar $destDir
done
