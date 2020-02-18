"""
11/29/2019
Import uvfits files to measurement sets. 
User inputs:
-n --fitsPath -<required> FULL path of fits file
-s --fileSuffix -<required> file suffix (e.g., .ms)

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--fitsPath', help = '<required> FULL path of fits file', required = True)
parser.add_argument('-s', '--fileSuffix', help= '<required> file suffix (e.g., .ms)', required = True)
args, unknown = parser.parse_known_args()

## parse name of visibiltiy from input path
fitsName = args.fitsPath.split('/')[-1]

## set split parameters and run
default('importuvfits')
print('writing to %s to ms file' % (fitsName))
fitsfile = args.fitsPath
vis = args.fitsPath.replace('.uvfits', args.fileSuffix)
importuvfits()
