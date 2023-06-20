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

## imports
import argparse
import glob 

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file_name', help = '<required> input file name (cleaned ASKAP cube)', required = True)
parser.add_argument('-o', '--out_file', help = '<required> name of output FITS cube', required = True)
parser.add_argument('-b', '--beam_file', help = '<required> name of input beam pattern cube', required = True)
parser.add_argument('-s', '--sd_file_name', help = '<required> name of input single dish file', required = True)
args, unknown = parser.parse_known_args()

## unpack user arguments
file_name = args.file_name
out_file = args.out_file
beam_file = args.beam_file
sd_file_name = args.sd_file_name

## make list to iterate over
fits_list = [file_name, sd_file_name]
casa_image_list = []

def main():

	## import fits 
	for fits in fits_list:
		importfits_params = {
			'imagename':fits.replace('.fits', '.im'),
			'fitsimage':fits}
		#importfits(**importfits_params)
		casa_image_list.append(fits.replace('.fits', '.im'))

	## smooth input askap image to 30''
	imsmooth_params = {
		'imagename':casa_image_list[0],
		'major':'30arcsec',
		'minor':'30arcsec',
		'pa':'0deg',
		'targetres':True,
		'outfile':'%s' % casa_image_list[0].replace('.im', '.imsmooth')}
	#imsmooth(**imsmooth_params)

	## correct for primary beam 
	image_list = [casa_image_list[0].replace('.im', '.imsmooth'), beam_file]
	immath_params = {
		'imagename':image_list, 
		'outfile':casa_image_list[0].replace('.im', '.imsmooth.pbc'),
		'expr':'IM0/(IM1/max(IM1))',
		'imagemd':image_list[0]}
	immath(**immath_params)

	## regrid single dish data
	regrid_params = {
		'imagename': casa_image_list[1],
		'output': casa_image_list[1].replace('.im', '.regrid'),
		'template':casa_image_list[0].replace('.im', '.imsmooth.pbc')}
	imregrid(**regrid_params)

	## run feather
	feather_params = {
		'highres':casa_image_list[0].replace('.im', '.imsmooth.pbc'),
		'lowres':casa_image_list[1].replace('.im', '.regrid'),
		'sdfactor':1.0,
		'imagename':out_file}

	## exportfits
	final_cube_name = '%s.fits' % (out_file)
	exportfits_params = {
		'imagename':out_file,
		'fitsimage':final_cube_name,
		'dropdeg':True,
		'dropstokes':True,
		'history':False,
		'velocity':True}
	exportfits(**exportfits_params)

if __name__=='__main__':
	main()
	exit()
