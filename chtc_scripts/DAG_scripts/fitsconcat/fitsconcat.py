"""
17/6/24
script based on Krishna Sekhar's script to concat individual spectral planes into PPV cube
see: https://github.com/Kitchi/fitsconcat/tree/main
User inputs:

Usage: 
python fitsconcat.py 
__author__ = "Nick Pingel"
__version__ = "1.0"
__email__ = "nmpingel@wisc.edu"
"""

##imports
import os
import glob
import argparse
import numpy as np
from astropy.io import fits

## parse user arguments
def parse_user_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path', help = '<required> path to input FITS files', required = True)
	parser.add_argument('-e', '--extension', help = '<required> is the suffix *-beam.fits or *-image-pb.fits; valid input is beam or image-pb', required = True)
	parser.add_argument('-o', '--outname', help ='<required> output name of file (.fits automatically appended)', required = True)
	args, unknown = parser.parse_known_args()
	return args.path, args.outname, args.extension

## make empty FITS cube
def make_empty_image(imlist, path, outname):
	"""
	Generate an empty dummy FITS data cube. The FITS cube can exceed available
	RAM.

	The 2D image dimensions are derived from the first image in the list.
	The number of channels in the output cube is assumed to be the length
	of the input list of images.
	"""

	with fits.open(imlist[0], memmap=True) as hud:
		xdim, ydim = np.squeeze(hud[0].data).shape[-2:]

	zdim = int(len(imlist))
	dims = tuple([zdim, ydim, xdim])
	print("X-dimension: ", xdim)
	print("Y-dimension: ", ydim)
	print("Z-dimension: ", zdim)
	print('\n')

	# create dummy header
	dummy_data = np.zeros(dims, dtype=np.float32)
	hdu = fits.PrimaryHDU(data=dummy_data)
	header = hdu.header
	fits.writeto('%s/%s' % (path, outname), dummy_data, header = header)

## fill cube with FITS images
def fill_cube_with_images(imlist, path, outname):
	"""
	Fills the empty data cube with fits data.

	The number of channels in the output cube is assumed to be the length
	of the input list of images.
	"""
	## open first image FITS to get header
	first_im_hdu = fits.open(imlist[0])

	## open cube FITS
	outhdu = fits.open('%s/%s' % (path, outname), memmap=True, mode="update")
	outdata = outhdu[0].data

	max_chan =  int(len(imlist))
	for ii in range(0, max_chan):
		print(f"Processing channel {ii}/{max_chan}", end='\r')
		with fits.open(imlist[ii], memmap=True) as hdu:
			print(hdu[0].data.shape)
			outdata[ii, :, :] = hdu[0].data[0, 0, :, :]
	## update fits file
	fits.writeto('%s/%s' % (path, outname), outdata, header = first_im_hdu[0].header, overwrite = True)
	outhdu.close()

def main():
	## parse user arguments (path to FITS files)
	fits_file_path, f_outname, f_ext = parse_user_arguments()
	cube_outname = '%s-%s.fits' % (f_outname, f_ext)
	image_list = sorted(glob.glob('%s/*-%s.fits' % (fits_file_path, f_ext)))

	## make empty FITS cube
	make_empty_image(image_list, fits_file_path, cube_outname )

	## fill FITS cube
	fill_cube_with_images(image_list, fits_file_path, cube_outname)
if __name__ == '__main__':
	main()