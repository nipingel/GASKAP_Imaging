"""
10/11/2019
Script to generate a list of all MS files associated with a given GASKAP field. The aim to be generic enough
such that one only needs to change the schedule block ID, interleave name, and master path to the calibrated
visibilities. No user inputs. 

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""



SBArr = ['4567', '4570', '4577']
for SB in SBArr:
	for i in range(0, 36):
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)
		visList.append('../data/oldSMC/%s/orig/SMC_%s_beam%s.ms' % (SB, SB, beamStr))
