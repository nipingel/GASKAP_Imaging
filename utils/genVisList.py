"""
10/11/2019
Script to generate a list of all MS files associated with a given GASKAP field. The aim to be generic enough
such that one only needs to change the schedule block ID, field name, and master path to the calibrated
visibilities. Potential user inputs:
-s --startBeam - If only a subset of beams are required, the user can provide starting & ending beam numbers 
-e --endBeam - ending beam 
-d --subDir - sub-directory to look for ms files (e.g., BINNED)

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
## imports
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--startBeam', help='starting beam', type = int)
parser.add_argument('-e', '--endBeam', help = 'ending beam', type = int)
parser.add_argument('-d', '--subDir', help = 'sub-directory to look for files')
args, unknown = parser.parse_known_args()
## default to 0-36 if not specified startBeam or endBeam
if not args.startBeam:
	startBeam = 0
	endBeam = 36
else:
	startBeam = args.startBeam
	endBeam = args.endBeam

dataPath = '/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered/'
SBID = '8906'
fieldName = 'SMC1-0_M344-11'
interleaveList = ['A', 'B', 'C']

## initialize empty list to store ms files
visList = []

## loop through the interleaves and beams to append to list
for inter in interleaveList:
	for i in range(startBeam, endBeam):
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)
		if not args.subDir: ## create list of unbinned calibratred visibilties 
			msFile = dataPath + '%s/%s%s/scienceData_SB%s_%s%s.beam%s_SL.ms' % \
			(SBID, fieldName, inter, SBID, fieldName, inter, beamStr)
		elif args.subDir == 'CONTSUB': ## create list of binned, continuum subtracted visibilities
			msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL_BINNED.ms.contsub' % \
                        (SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr)
	        else: ## create list of binned visibilities
                        msFile = dataPath + '%s/%s%s/%s/scienceData_SB%s_%s%s.beam%s_SL_BINNED.ms' % \
                        (SBID, fieldName, inter, args.subDir, SBID, fieldName, inter, beamStr)
		visList.append(msFile)
