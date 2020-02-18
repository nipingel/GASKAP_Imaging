"""
11/28/2019
Split input ms by input time range string
User inputs:
-t --timeRange -<required> time string over which to split out the visibiltities; (i.e., YYYY/MM/DD/hh:mm:ss~YYYY/MM/DD/hh:mm:ss)
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
parser.add_argument('-t', '--timeRange', help='<required> time string over which to split out the visibiltities; (i.e., YYYY/MM/DD/hh:mm:ss~YYYY/MM/DD/hh:mm:ss)', required = True)
parser.add_argument('-n', '--msPath', help = '<required> FULL path of ms file', required = True)
args, unknown = parser.parse_known_args()

## get number of channels to use in average
timeRange = args.timeRange

## parse name of visibiltiy from input path
msName = args.msPath.split('/')[-1]

## set split parameters and run
default('split')
print('Splitting out %s from %s ' % (timeRange, msName))
vis = args.msPath
outputvis = args.msPath + '.timeSplit'
timerange = timeRange
datacolumn = 'data'
split()
