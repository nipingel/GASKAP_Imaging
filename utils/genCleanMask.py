"""
03/18/2021
Script to generate a clean mask from list of files from a user provided extension (e.g., '.image') and postive/negative threshold level, 
which denotes the minimum absorbed and emission pixel values to be included in the clean mask. Generally ~2x the noise
These masks will then be used by tclean to continue cleaning/imaging. 

** MUST BE RUN IN SAME DIRECTORY AS INPUT FILES **

User inputs:
-f --fileExt - <required> file extension (e.g., 'image')
-t --threshold - <required> minimum emission pixel value to include in mask 
-n --abs_threshold - <optional> minimum absorbed piixel value to include in mask

__author__="Nickolas Pingel"
__email__="Nickolas.Pingel@anu.edu.au"
"""

### imports
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileExt', help = '<required> file extension (e.g., image)', required = True)
parser.add_argument('-t', '--threshold', help = '<required> minimum pixel value to include in mask', required = True)
parser.add_argument('-n', '--abs_threshold', help = '<optional>minimum absorbed piixel value to include in mask', required = True)


args, unknown = parser.parse_known_args()

fileExt = args.fileExt
threshold = args.threshold
abs_threshold = args.abs_threshold

if abs_threshold is not None:
	print('Creating mask from emission pixels with values at and above %s [Jy/Beam]' % threshold)
	print('Including absorbed pixels with values at and below %s [Jy/Beam]' % abs_threshold)
else:
	print('Creating mask from just emission pixels with values at and above %s [Jy/Beam]' % threshold)

## create list of files
fileList = glob.glob('*.%s' % fileExt)

## sort numerically
fileList.sort()

## loop through list to make mask based on threshold
for file in fileList:
	print('Generating mask for file: %s' % file)

	if abs_threshold is not None:
		## make internal mask based on absorption/emission thresholds
		ia.open(file)
		ia.calcmask(mask = '%s > %s || %s < %s' % (file, threshold, file, abs_threshold), name = 'sig_2.0.mask')
		ia.done()
	else:
		## make internal mask based on absorption/emission thresholds
		ia.open(file)
		ia.calcmask(mask = '%s > %s' % (file, threshold), name = 'sig_2.0.mask')
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
