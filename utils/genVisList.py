"""
10/11/2019
Script to generate a list of all MS files associated with a given GASKAP field. The aim to be generic enough
such that one only needs to change the schedule block ID, field name, and master path to the calibrated
visibilities. Potential user inputs:
-s --startBeam - <optional> If only a subset of beams are required, the user can provide starting & ending beam numbers 
-e --endBeam - <optional>ending beam 
-d --subDir - <required> sub-directory to look for ms files (e.g., BINNED)
-b --skipBeam - <optional> list of beams to skip
-i --skipIter - <optional> list of interleaves to skip'
-c --chanNum - <optional> channel number if dealing with split ms files

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
## imports
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--startBeam', help='<optional> starting beam', type = int)
parser.add_argument('-e', '--endBeam', help = '<optional> ending beam', type = int)
parser.add_argument('-d', '--subDir', help = '<required> sub-directory to look for files', required = True)
parser.add_argument('-b', '--skipBeam', help ='<optional> list of beams to skip')
parser.add_argument('-i', '--skipInter', help = '<optional> list of interleaves to skip')
parser.add_argument('-c', '--chanNum', help='<optional> channel number if dealing with split ms files', type = int)
args, unknown = parser.parse_known_args()

## unpack arguments
skipBeamList = args.skipBeam
skipInterList = args.skipInter
print(skipBeamList[0], skipInterList[0])

## default to 0-36 if not specified startBeam or endBeam
if not args.startBeam:
	startBeam = 0
	endBeam = 36
else:
	startBeam = args.startBeam
	endBeam = args.endBeam + 1

dataPath = '/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered/'
SBID = '8906'
fieldName = 'SMC1-0_M344-11'
interleaveList = ['A', 'B', 'C']

## initialize empty list to store ms files
visList = []

## initialize beam/interleave skip boolean
skipBool = False
skipCnt = 0

## loop through the interleaves and beams to append to list
for i in range(startBeam, endBeam):
	for inter in interleaveList:
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)

		## determine whether if beam/interleave pair needs to be skipped
		if args.skipBeam:
			try:
				skipBeam = int(skipBeamList[skipCnt])
			except IndexError:
				pass

			## determine if interleaves need to be skipped
			if skipBeam == i:

				## set skip boolean variable to true
				skipBool = True
				skipInter = skipInterList[skipCnt]
				if inter in skipInter:
					continue

		if not args.subDir: ## create list of unbinned, non-continuum subtracted calibrated visibilties 
			msFile = dataPath + '%s/%s%s/scienceData_SB%s_%s%s.beam%s_SL.ms' % \
			(SBID, fieldName, inter, SBID, fieldName, inter, beamStr)
		
		## create list of binned, continuum subtracted visibilities
		if args.subDir == 'CONTSUB':
	    	## if args.chanNum is defined, then we are creating a list of files continuum subtracted and 
	    	## split out by channel number. If not defined, then we are creating a list of just continuum
	    	## subtracted files
			msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL_binned.contsub_chan%d.ms' % \
			(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr, args.chanNum)
	    	
	    	try:
	    		args.chanNum
	    	except NameError:
	    		msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL_binned.contsub' % \
				(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr)

		if args.subDir == 'TIME_SPLIT': 
			## create list of split out ms files (by time)
	    	## if args.chanNum is defined, then we are creating a list of files split out by channel number
	    	## and time if not defined, then we are creating a list of files just split out by time
			msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL.binned.contsub_split_chan%d.ms' % \
	    	(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr, args.chanNum)
	    	
	    	try:
	    		args.chanNum
	    	except NameError:
	    		msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL.binned.contsub_split.ms' % \
	    		(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr)
	    
		if args.subDir == 'BINNED': ## create list of binned visibilities
	    	## if args.chanNum is defined, then we are creating a list of files binned and split out by channel number.
	    	## If not defined, then we are creating a list of just binned files
			msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL.binned_chan%d.ms' % \
			(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr, args.chanNum)
	    	try:
	    		args.chanNum
	    	except NameError:
	    		msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL.binned_chan%d.ms' % \
	    		(SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr, args.chanNum)
		visList.append(msFile)

		## if we skipped a beam, increase skipped counter and reset boolean
		if skipBool == True:
			skipBool = False
			skipCnt+=1

