"""
06/7/2023
This script converts FITS files to CASA image files (replace .fits file extension with user provided file extension
User Inputs:
-f --file_name - <required> input file name
-e --extension - <required> file extension
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""

## imports
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file_name', help = '<required> input file name', required = True)
parser.add_argument('-e', '--extension', help = '<required> file extension', required = True)
args, unknown = parser.parse_known_args()

file_name = args.file_name
ext = args.extension

def main():

	importfits_params = {
		'fitsimage':file_name,
		'imagename':file_name.replace('.fits', '.%s' % ext)}
	importfits(**importfits_params)

if __name__=='__main__':
	main()
	exit()