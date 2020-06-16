"""
6/16/2020
script to configure the CASA task 'concat' to merge visibilities of the same beam and interleave from two separate SBIDs
User inputs:
-p1 --path1 -<required> FULL path to first ms file
-p2 --path2 -<required> FULL path of second ms file
-c --concat_path -<required> FULL path for concatenated ms file

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p1', '--path1', help='<required> FULL path to first ms file', required = True)
parser.add_argument('-p2', '--path2', help = '<required> FULL path to second ms file', required = True)
parser.add_argument('-c', '--concat_path', help = '<required> FULL path for concatenated msfile' , required = True)
args, unknown = parser.parse_known_args()

## parse name of first path to ms file
msName_1 = args.path1.split('/')[-1]

## parse name of first path to ms file
msName_2 = args.path2.split('/')[-1]

## construct list of visibilities to be concatenated
visList = []
visList.extend([args.path1, args2.path2])

## set split parameters and run
default('concat')
print('Concatenating %s and %s channels' % (msName_1, msName_2))
vis = visList
concatvis = args.concat_path
copypointing = False
concat()