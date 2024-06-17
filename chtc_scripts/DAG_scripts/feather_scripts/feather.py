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
fits_list = [file_name, sd_file_name, beam_file]
casa_image_list = []

def main():
	## import fits 
	for fits in fits_list:
		importfits_params = {
			'imagename':'%s.im' % fits,
			'fitsimage':fits}
		importfits(**importfits_params)

	## convert ASKAP-only cube from TOPOCENTRIC to LSRK
	imreframe_params = {
		'imagename':'%s.im' % fits_list[0],
		'output':'%s.im.lsrk' % fits_list[0],
		'outframe':'lsrk'
	}
	imreframe(**imreframe_params)
	
	## smooth input askap image to 30''
	imsmooth_params = {
		'imagename':'%s.im.lsrk' % fits_list[0],
		'major':'30arcsec',
		'minor':'30arcsec',
		'pa':'0deg',
		'targetres':True,
		'outfile':'%s.im.lsrk.imsmooth.pbc' % fits_list[0]}
	imsmooth(**imsmooth_params)

	## remove stokes axis in beam cube
	imsubimage_params = {
		'imagename':'%s.im' % fits_list[2],
		'outfile':'%s.im.bm' % fits_list[2],
		'dropdeg':True,
		'overwrite':True}
	imsubimage(**imsubimage_params)

	## regrid single dish data
	regrid_params = {
		'imagename':'%s.im' % fits_list[1],
		'output': '%s.im.regrid' % fits_list[1],
		'template':'%s.im.lsrk.imsmooth.pbc' % fits_list[0]}
	imregrid(**regrid_params)

	## run feather
	feather_params = {
		'highres':'%s.im.lsrk.imsmooth.pbc' % fits_list[0],
		'lowres':'%s.im.regrid' % fits_list[1],
		'sdfactor':1.0,
		'imagename':out_file}
	feather(**feather_params)

    ## run immath again to mask out pixels outside primary beam area
    mask_list = [out_file, '%s.im.bm' % fits_list[2]] 
    immath_mask_params = {
        'imagename': mask_list,
        'outfile': '%s.clipped' % out_file,
        'expr': 'iif(IM1 > 0.05, IM0, 0.0)',
        'imagemd':fits_list[0]}
    immath(**immath_mask_params)

    ## exportfits
	final_cube_name = '%s.fits' % ('%s.clipped' % out_file)
	exportfits_params = {
		'imagename':'%s.clipped' % out_file,
		'fitsimage':final_cube_name,
		'dropdeg':True,
		'dropstokes':True,
		'history':False,
		'velocity':True}
	exportfits(**exportfits_params)

if __name__=='__main__':
	main()
	exit()