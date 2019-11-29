"""
11/20/2019
Split out a user provided channel fromj input ms file
User inputs:
-n --msPath -<required> FULL path of ms file
-c --chanNum -<required> channel to split out
__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--msPath', help = '<required> FULL path of ms file', required = True)
parser.add_argument('-c', '--chanNum', help='<required> channel to split out', required = True)
args, unknown = parser.parse_known_args()

## get number of channels to use in average
chanNum = args.chanNum

## parse name of visibiltiy from input path
msName = args.msPath.split('/')[-1]

## determine file suffix
fileSuffix = msName.split('.')[-1]

## set split parameters and run
default('split')
print('Splitting out channel %s from %s ' % (chanNum, msName))
vis = args.msPath
outputvis = args.msPath.replace('.' + fileSuffix, '_chan%s.ms' % chanNum)
spw='0:%s' % chanNum
datacolumn = 'data'
split()
