"""
12/13/2019
Script to generate a text file with all beam phase centers from an ASKAP SBID. Must be run within an aces virtual environment (e.g, source ../misc/initaces.sh)
User inputs:
-s --subDir - <required> sub-directory to look for ms files 
-b --sbID - <required> name of SBID (e.g., 8906)
-f --fieldName - <required> name of field (e.g., SMC1-0_M334-11)



__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
## imports
import argparse
from casacore.tables import *
import astropy.units as u
from astropy.coordinates import SkyCoord
import glob as glob

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subDir', help='<required> sub-directory to look for ms files', required = True)
parser.add_argument('-b', '--sbID', help ='<required> name of SBID (e.g., 8906)', required = True)
parser.add_argument('-f', '--fieldName', help = 'name of field (e.g., SMC1-0_M334-11)', required = True)
args, unknown = parser.parse_known_args()

## unpack user arguments
subDir = args.subDir 
SBID = args.sbID
fieldName = args.fieldName
interleaveList = ['A', 'B', 'C']

## open file
f = open('phaseCenters_%s_%s.txt' % (fieldName, SBID), "w")

## loop through files, select the Ra/Dec from REFERENCE_DIR in FIELD table based on FIELD_ID, convert to hh:mm:ss format and write to file
for inter in interleaveList: 
	for i in range(0, 36):
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)
                msFile = '%s/%s/%s/%s%s/scienceData_SB%s_%s%s.beam%s_SL.ms' % (subDir, SBID, fieldName, fieldName, inter, SBID, fieldName, inter, beamStr)
		#msFile = '%s/scienceData_SB%s_%s%s.beam%s_SL.ms' % (subDir, SBID, fieldName, inter, beamStr)

		## open table in read-only to get FIELD_ID
		t = table(msFile)
		fieldIDCol = t.getcol('FIELD_ID')
		fieldIDVal = fieldIDCol[0] ## same for all rows
		t.close()

		## open FIELD table to get phase center
		tF = table('%s/FIELD' % msFile)
		phaseDir = tF.getcol('REFERENCE_DIR')
		phaseVal = phaseDir[fieldIDVal][0]
		c = SkyCoord(phaseVal[0], phaseVal[1], unit = 'rad', frame = 'icrs')
		print('Phase center of %s: %s' % (msFile, c.to_string('hmsdms')))
		tF.close()

		## write to open file 
		writeStr = '%s: %s\n' % (msFile.split('/')[-1], c.to_string('hmsdms'))
		f.write(writeStr)
f.close()


