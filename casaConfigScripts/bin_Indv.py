"""
11/13/2019
Bin channel range by user provided integer. 
User inputs:
-w --width -<required> integer number of channels to average over to create new output channel
-n --msPath -<required> FULL path of ms file

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--width', help='<required> integer number of channels to average over to create new output channel', type = int, required = True)
parser.add_argument('-n', '--msPath', help = '<required> FULL path of ms file', required = True)
args, unknown = parser.parse_known_args()

## get number of channels to use in average
widthChans = args.width

## parse name of visibiltiy from input path
msName = args.msPath.split('/')[-1]

## set split parameters and run
default('split')
print('Binning %s by %d channels' % (msName, widthChans))
vis = args.msPath
outputvis = args.msPath.replace('.ms', '.binned')
width = 2
datacolumn = 'data'
split()
