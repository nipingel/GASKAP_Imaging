"""
6/6/2023
generate a clean mask based on the input beam pattern from WSCLEAN 

User inputs:
-n --name - <required> name of input beam pattern fits file
-o --output - <required> name of output FITS file
-t --threshold - <required> minimum primary beam response level pixel to include in mask'

__author__="Nickolas Pingel"
__email__="nmpingel@wisc.edu"
"""

### imports
import argparse
from astropy.io import fits
import numpy as np 
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help = '<required> name of input beam pattern fits file', required = True)
parser.add_argument('-t', '--threshold', help = '<required> minimum primary beam response level pixel to include in mask', required = True)
parser.add_argument('-o', '--output', help = '<required> name of output FITS file', required = True)
args, unknown = parser.parse_known_args()

## assign user variables
image_name = args.name
threshold = float(args.threshold)
output_name = args.output

## read in data
image_hdu = fits.open(image_name)
image_data = image_hdu[0].data

## make copy of input primary beam image
mask_data = np.zeros_like(image_data)

## give pixels that are above given threshold a value of 1.0 to mark cleaning region
good_indices = np.where(image_data > threshold)
mask_data[good_indices] = 1.0

## write out new image
fits.writeto('%s.fits' % output, data = mask_data, header = image_hdu[0].header)