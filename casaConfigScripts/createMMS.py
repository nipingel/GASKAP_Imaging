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

## call genVisList.py to create list of visibiltities called 'visList'
execfile('genVisList')

## initialize the virtualconcat task
default('virtualconcat')

## set parameters
vis = visList
concatvis = 'SB8906_allBeams_interleavesABC.mms'
keepcopy = False
virtualconcat()
