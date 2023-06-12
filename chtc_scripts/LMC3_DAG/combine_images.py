"""
05/23/2023
This script takes a user provided file extension (e.g., '.image'), compiles a list, and iterively 
hacks each file's metadata. The parameters that will be corrected (can also be specified by the user): 
rest frequency and frequency resolution. Once the headers are corrected, The images are then
combined, converted to LSRK reference frame, and written to a FITS file. 
User Inputs:
-f --fileExt - <required> file extension (e.g., 'image')
-d --freqRes - <required> frequency resolution in kHz
-o --outFile - <required> name of FITS cube
-r --restFreq - rest frequency in MHz (default is 1420.405752)
__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""

## imports
import argparse
import glob 

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileExt', help = '<required> file extension (e.g., image)', required = True)
parser.add_argument('-d', '--freqRes', help = '<required> frequency resolution in kHz', required = True)
parser.add_argument('-o', '--outFile', help = '<required> name of FITS cube', required = True)
parser.add_argument('-r', '--restFreq', help = 'rest frequency in MHz (default is 1420.405752)', default = '1420.405752')
args, unknown = parser.parse_known_args()

## unpack user arguments
fileExt = args.fileExt
restFreqStr = '%sMHz' % args.restFreq
freqResStr = '%skHz' % args.freqRes
outFile = args.outFile

## create list of files
fileList = glob.glob('*.%s' % fileExt)

## ensure list is in ascending channel order
fileList.sort()

## loop through list to correct headers
for file in fileList:
	## set rest freq
	imhead(imagename = file, mode = 'put', hdkey = 'restfreq', hdvalue = restFreqStr)

	## set frequency resolution
	imhead(imagename = file, mode = 'put', hdkey = 'cdelt3', hdvalue = freqResStr)

## combine images
ia.imageconcat(outfile = '%s.combImage' % outFile , infiles = fileList, relax = False)

imreframe(imagename = '%s.combImage' % outFile, output = '%s_lsrk.combImage' % outFile, outframe = 'lsrk')

## write out FITS file
exportfits(imagename = '%s_lsrk.combImage' % outFile, fitsimage = '%s_lsrk.fits' % outFile, velocity = True, dropdeg = True, history = False)
