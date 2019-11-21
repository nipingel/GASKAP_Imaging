"""
10/11/2019
CASA config file to create Multi-Measurement Set file containing all 108 calibrated, 
continuum subtracted, and binned visibilties from a single ASKAP field, This calls an 
external python script to generate the input list of visibilties before running the 
task 'virtualconcat'. There are no user inputs, but one should rename the 'concatvis'
parameter to an appropriate name. 

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""

## set path for output MMS file
outputPath = '/avatar/nipingel/ASKAP/SMC/data/smc2019/msdata_smc/altered'
SBID = '8906'

## set genVistList parameters
startBeam = '0'
endBeam = '35'
subDir = 'CONTSUB'

## call genVisList.py to create list of visibiltities called 'visList'
sys.argv = ['../utils/genVisList.py', '-s', startBeam, '-e', endBeam, '-d', subDir]
execfile('../utils/genVisList.py')

## initialize the virtualconcat task
default('virtualconcat')

## set parameters
vis = visList
concatvis = '%s/%s/SB8906_allBeams_interleavesABC.mms' % (outputPath, SBID)
keepcopy = False
copypointing = False
virtualconcat()
