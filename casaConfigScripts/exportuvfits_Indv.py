"""
11/28/2019
Export input ms to uvfits format. This is also a work around to split out a specific time range
when split/mstransform complains about row access to the deleted POINTING sub-table
User inputs:
-n --msPath -<required> FULL path of ms file
-t --timeRange -<optional> time string over which to split out the visibiltities; (i.e., YYYY/MM/DD/hh:mm:ss~YYYY/MM/DD/hh:mm:ss)


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
parser.add_argument('-t', '--timeRange', help='<optional> time string over which to split out the visibiltities; (i.e., YYYY/MM/DD/hh:mm:ss~YYYY/MM/DD/hh:mm:ss)')
args, unknown = parser.parse_known_args()

## parse name of visibiltiy from input path
msName = args.msPath.split('/')[-1]

## get number of channels to use in average
timeRange = args.timeRange

## set split parameters and run
default('exportuvfits')
print('writing to %s to uvfits file' % (msName))
vis = args.msPath
fitsfile = args.msPath + '.uvfits'
## set timerange, if define
try:
	timeRange
except NameError:
	pass
else:
	print('Splitting out time range: %s' % (timeRange))
	timerange = timeRange
datacolumn = 'data'
exportuvfits()
