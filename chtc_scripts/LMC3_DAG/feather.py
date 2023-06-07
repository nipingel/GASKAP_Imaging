"""
06/6/2023
This script creates a smoothed, primary beam corrected, feathered, and masked GASKAP cube
User Inputs:
-f --file_name - <required> input file name (cleaned ASKAP cube)
-o --out_file- <required> name of output FITS cube
-b --beam_cube_name - <required> name of input beam pattern cube
-s --sd_files_name - <required> name of input single dish file
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""


-f ${file_name} -o ${output_name} -b ${beam_cube_name} -s ${sd_file_name}

## imports
import argparse
import glob 

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file_name', help = '<required> input file name (cleaned ASKAP cube)', required = True)
parser.add_argument('-o', '--out_file', help = '<required> name of output FITS cube', required = True)
parser.add_argument('-b', '--beam_cube_name', help = '<required> name of input beam pattern cube', required = True)
parser.add_argument('-s', '--sd_files_name', help = '<required> name of input single dish file', required = True)

args, unknown = parser.parse_known_args()

## unpack user arguments
file_name = args.file_name
out_file = args.out_file
beam_file = args.beam_file
sd_file_name = args.sd_file_name

## make list to iterate over
fits_list = [file_name, beam_file, sd_file_name]

def main():

	## import fits 
	for fits in fits_list:
		importfits__params = {
			'imagename':fits.replace('.fits', '.im'),
			'fitsimage':fitsimage}
		imporfits(**importfits_params)

	## smooth input askap image to 30''
	imsmooth_params = {
		'imagename':file_name,
		'major':'30arcsec',
		'minor':'30arcsec',
		'bpa':'0deg',
		'targetres':True,
		'outfile':'%s.imsmooth' % file_name}
	imsmooth(**imsmooth_params)

	## correct for primary beam 
	smoothed_file_name = '%s.imsmooth' % file_name
	image_list = [smoothed_file_name , beam_file]
	immath_params = {
		'images':image_list, 
		'outfile':'%s.imsmooth.pbc' % (file_name),
		'expr':'IM0/IM1'
	}
	pbc_file = '%s.imsmooth.pbc' % (file_name)
	immath(**immath_params)

	## run feather
	feather_params = {
		'highres':pbc_file,
		'lowres':sd_file_name,
		'sdfactor':1.0,
		'imagename':outfile}

	## exportfits
	final_cube_name = '%s.fits' % (outfile)
	exportfits_params = {
		'imagename':outfile,
		'fitsimage':final_cube_name,
		'dropdeg':True,
		'dropstokes':True,
		'history':False,
		'velocity':True}
	exportfits(**exportfits_params)

if __name__=='__main__':
	main()
	exit()