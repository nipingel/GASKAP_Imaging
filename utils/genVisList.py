"""
10/11/2019
Script to generate a list of all MS files associated with a given GASKAP field. The aim to be generic enough
such that one only needs to change the schedule block ID, field name, and master path to the calibrated
visibilities. No user inputs. 

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""

dataPath = '/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered/'
SBID = '8906'
fieldName = 'SMC1-0_M344-11'
interleaveList = ['A', 'B', 'C']

## initialize empty list to store ms files
visList = []

## loop through the interleaves and beams to append to list
for inter in interleaveList:
	for i in range(0, 36):
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)
		msFile = dataPath + '%s/%s%s/CONTSUB/scienceData_SB%s_%s%s.beam%s_SL_BINNED.ms.contsub' % \
		(SBID, fieldName, inter, SBID, fieldName, inter, beamStr)
		visList.append(msFile)

