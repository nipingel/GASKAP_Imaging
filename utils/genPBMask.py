"""
11/13/2020
Mask an input cube based on a user defined primary beam threshold. For exampe, all pixels corresponding to a primary
beam response of at and above 0.5 will be kept. The final image is trimmed to throw away blanked pixels. 

User inputs:
-i --imageCube - <required> path to image cube
-p --pbCube - <required> path to primary beam cube (MUST HAVE SAME DIMENSIONS AS INPUT IMAGE CUBE)
-t --threshold - <required> minimum primary beam response level pixel to include in mask 
-o --output - <required> name of output image

__author__="Nickolas Pingel"
__email__="Nickolas.Pingel@anu.edu.au"
"""

### imports
import argparse
from astropy.io import fits
import numpy as np 
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--imageCube', help = '<required> full path to image cube', required = True)
parser.add_argument('-p', '--pbCube', help = '<required> full path to primary beam cube (MUST HAVE SAME DIMENSIONS AS INPUT IMAGE CUBE)', required = True)
parser.add_argument('-t', '--threshold', help = '<required> minimum primary beam response level pixel to include in mask', required = True)
parser.add_argument('-o', '--output', help = '<required> name of output file', required = True)

args, unknown = parser.parse_known_args()

image_path = args.imageCube
pbCube_path = args.pbCube
threshold = float(args.threshold)
output = args.output

print('Creating mask from pixels with PB values at and above %s' % threshold)

## read in image and pb cubes
try:
	image_hdu = fits.open(image_path)
	pb_hdu = fits.open(pbCube_path)
except FileNotFoundError:
	print('Path to image or PB cube is incorrect; exiting...')
	sys.exit()

image_data = image_hdu[0].data
pb_data = pb_hdu[0].data

## check whether there is:
## 		degenerate stokes axis
## 		that the images are the same size 
if len(image_data.shape) > 3:
	image_data = image_data[0, :, :, :]
if len(pb_data.shape) > 3:
	pb_data = pb_data[0, :, :, :]

compareShape_bool = image_data.shape == pb_data.shape
if compareShape_bool == False:
	raise IndexError("Image and PB cubes are not the same shape")

## now, determine which pixels are below user threshold
bad_pb_indices = np.where(pb_data < threshold)

## set these equal to 0 in data image
image_data[bad_pb_indices] = np.float('nan')

## write out new image
fits.writeto('%s.fits' % output, data = image_data, header = image_hdu[0].header)




