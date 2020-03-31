"""
04/01/2020
Script to generate a clean mask from list of files from a user provided extension (e.g., '.image') and threshold level, 
which denotes the minimum pixel value to be included in the clean mask. Generally ~2x the noise
These masks will then be used by tclean to continue cleaning/imaging. 

User inputs:
-f --fileExt - <required> file extension (e.g., 'image')
-t --threshold - <required> minimum pixel value to include in mask 

__author__="Nickolas Pingel"
__email__="Nickolas.Pingel@anu.edu.au"
"""

### imports
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileExt', help = '<required> file extension (e.g., image)', required = True)
parser.add_argument('-t', '--threshold', help = '<required> minimum pixel value to include in mask', required = True)

args, unknown = parser.parse_known_args()

fileExt = args.fileExt
threshold = args.threshold

print('Creating mask from pixels with values at and above %s [Jy/Beam]' % threshold)

## create list of files
fileList = glob.glob('../casaConfigScripts/*.%s' % fileExt)

## sort numerically
fileList.sort()

## loop through list to make mask based on threshold
#for file in fileList:
for i in range(0, 1):
	file = fileList[i]
	print('Generating mask for file: %s' % file)
	
	## make internal mask based on threshold
	ia.open(file)
	ia.calcmask(mask = '%s > %s' % (file, threshold), name = 'sig_2.0_mask')
	ia.done()

	## generate actual 1/0 mask image
	default('makemask')
	mode = 'copy'
	output = file.replace(fileExt, 'mask')
	inpimage = file
	inpmask = '%s:sig_2.0.mask' % file
	makemask()

	## delete internal mask
	default('makemask')
	mode = 'delete'
	inpmask = '%s:sig_2.0.mask' % file
	makemask()