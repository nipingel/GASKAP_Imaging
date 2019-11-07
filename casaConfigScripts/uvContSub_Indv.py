"""
10/31/2019
Perform continuum subtraction by fitting low order polynomial over a range of required input list of 
channels, polynomial fit order, and full path of ms file name. 
User inputs:
-l --listOfChans - list of channels over which a low order polynomial is fit
-o --order -order of fitting polynomial 
-n --msPath -path of measurement set

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--listOfChans', nargs='+', help='<required> list of channels over which a low order polynomial is fit', required=True)
parser.add_argument('-o', '--order', help='<required> order of fitting polynomial', type = int, required = True)
parser.add_argument('-n', '--msPath', help = '<required> FULL path of ms file', required = True)
args, unknown = parser.parse_known_args()

## based on list of channels, create string to pass to 'fitspw' uvcontsub3 task
listOfChans = args.listOfChans
fitspwStr = '0:'
for i in range(len(args.listOfChans)):
	## unpack value
	chanVal = args.listOfChans[i]
	fitspwStr += chanVal

	## check whether starting or ending channel of pair. 
	## if starting, add ~; if end add ';'; do nothing
	## if last channel in list
	if i % 2 == 0:
		fitspwStr += '~'
	elif i % 2 == 1 and i < len(args.listOfChans) - 1:
		fitspwStr += ';'
print('Fitting over this spw and channels: %s' % fitspwStr)

## parse name of visibiltiy from input path
msName = args.msPath.split('/')[-1]

## set uvcontsub3 parameters and run
default('uvcontsub')
print('Removing continuum from: %s' % msName)
vis = args.msPath
fitspw = fitspwStr
fitorder = args.order
uvcontsub()
