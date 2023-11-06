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
		importfits(**importfits_params)
		casa_image_list.append(fits.replace('.fits', '.im'))
		
	
	## smooth input askap image to 30''
	imsmooth_params = {
		'imagename':casa_image_list[0],
		'major':'30arcsec',
		'minor':'30arcsec',
		'pa':'0deg',
		'targetres':True,
		'outfile':'%s' % casa_image_list[0].replace('.im', '.imsmooth')}
	imsmooth(**imsmooth_params)

	## remove stokes axis in beam cube
	beam_file_imsub = '%s.imsub' % beam_file
	imsubimage_params = {
		'imagename':beam_file,
		'outfile':beam_file_imsub,
		'dropdeg':True,
		'overwrite':True}
	imsubimage(**imsubimage_params)

	## correct for primary beam 
	askap_image_list = [casa_image_list[0].replace('.im', '.imsmooth'), beam_file_imsub]
	immath_params = {
		'imagename':askap_image_list, 
		'outfile':casa_image_list[0].replace('.im', '.imsmooth.pbc'),
		'expr':'IM0/(IM1/max(IM1))',
		'imagemd':askap_image_list[0]}
	immath(**immath_params)

	## replace askap_image_list with primary beam corrected images
	askap_image_list = [casa_image_list[0].replace('.im', '.imsmooth.pbc'), beam_file_imsub]
	## run immath again to mask out pixels outside primary beam area
	immath_mask_params = {
		'imagename': askap_image_list,
		'outfile': askap_image_list[0].replace('.imsmooth.pbc', '.imsmooth.pbc.clipped'),
		'expr': 'iif(IM1 > 0.25, IM0, 0.0)',
		'imagemd':askap_image_list[0]}
	immath(**immath_mask_params)

	## regrid single dish data
	regrid_params = {
		'imagename': casa_image_list[1],
		'output': casa_image_list[1].replace('.im', '.regrid'),
		'template':casa_image_list[0].replace('.im', '.imsmooth.pbc.clipped')}
	imregrid(**regrid_params)

	## run feather
	feather_params = {
		'highres':casa_image_list[0].replace('.im', '.imsmooth.pbc.clipped'),
		'lowres':casa_image_list[1].replace('.im', '.regrid'),
		'sdfactor':1.0,
		'imagename':out_file}

	feather(**feather_params)
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
