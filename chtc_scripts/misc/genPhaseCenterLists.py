"""
8/11/2021
Script that generates a text file of beam phase centers based on a list of MS files. The user must provide 
the phase centers for each interleave as input
-p --path - <required> path to directory containing MS files
-e --suffix - <optional> file suffix for MS file (default *.ms)
-o --output - <required> name of output file to store beam phase centers
-a --interA - <required> center coordinate for A interleave (J2000, MUST be in 00h00m00.0s 00d00m00.0s format)
-b --interB - <required> center coordinate for B interleave (J2000, MUST be in 00h00m00.0s 00d00m00.0s format)
-c --interC - <required> center coordinate for C interleave (J2000, MUST be in 00h00m00.0s 00d00m00.0s format)
__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
## imports
import argparse
from casacore.tables import *
import astropy.units as u
import re
#from askap.footprint import Skypos
from Skypos import Skypos
from astropy.coordinates import SkyCoord
import glob as glob

## parse user arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='<required> path to directory containing MS files', required = True)
parser.add_argument('-s', '--suffix', help='<optional> file suffix for MS file (default *.ms)', required = False, default = 'ms')
parser.add_argument('-o', '--output', help='<required> name of output file to store beam phase centers', required = True)
parser.add_argument('-a', '--inter_A', help='<required> center coordinate for A interleave (J2000, MUST be in 00h00m00.0s,00d00m00.0s format)', required = True)
parser.add_argument('-b', '--inter_B', help='<required> pcenter coordinate for B interleave (J2000, MUST be in 00h00m00.0s,00d00m00.0s format)', required = True)
parser.add_argument('-c', '--inter_C', help='<required> center coordinate for C interleave (J2000, MUST be in 00h00m00.0s,00d00m00.0s format)', required = True)
args, unknown = parser.parse_known_args()

## unpack user arguments
path = args.path
suffix = args.suffix
output_name = args.output
inter_A = args.inter_A
inter_B = args.inter_B
inter_C = args.inter_C

## define lists to hold interleave coordinates
inter_list = [inter_A, inter_B, inter_C]
inter_ra_list = []
inter_dec_list = []

## check that user provided phase centers are formatted correctly
for inter in inter_list:
	inter_ra_dec = inter.split(',')
	inter_ra = re.split('h|m|s', inter_ra_dec[0])
	inter_dec = re.split('d|m|s', inter_ra_dec[1])

	if len(inter_ra) == 1 or len(inter_dec) == 1:
		raise SyntaxError('Coordinates for interleave phase center are not formatted correctly', inter_ra, inter_dec)
		sys.exit()

	else:
		inter_ra_list.append(inter_ra_dec[0])
		inter_dec_list.append(inter_ra_dec[1])


## construct list of MS files
print('%s/*.%s' % (path, suffix))
ms_file_list = sorted(glob.glob('%s/*.%s' % (path, suffix)))
## open file for writing 
f = open('%s.txt' % output_name, "w")

for ms_file in ms_file_list:
	## Open up MS MAIN table so it can be read
	main_table = table(ms_file, readonly = True, ack = False)
	## Open up the MS FIELD table so it can be read
	field_table = table("%s/FIELD" % (ms_file), readonly=True, ack=False)
	## Open up the MS FEED table so we can work out what the offset is for the beam.
	feed_table = table("%s/FEED" % (ms_file), readonly=True, ack=False)

	## get beam number
	vis_feed = main_table.getcol('FEED1', 0, 1)
	beam = vis_feed[0]

	## get field ID from first row of FIELD_ID column in main table
	## open table in read-only to get FIELD_ID
	field_id_col = main_table.getcol('FIELD_ID')
	field_id = field_id_col[0] ## same for all rows
	
	## get offsets from FEED table
	# The offsets are assumed to be the same for all antennas so get a list of all
	# the offsets for one antenna and for the current beam. This should return offsets
	# required for each field.
	feed_table_filtered = taql("select from $feed_table where ANTENNA_ID==0 and FEED_ID==$beam")
	offset = feed_table_filtered.getcol("BEAM_OFFSET")[field_id]

	## loop through the interleave coordinates and calculate offset
	inter_phase_center = SkyCoord(inter_ra_list[field_id], inter_dec_list[field_id], frame = 'icrs')
	inter_phase_center_rad = Skypos(inter_phase_center.ra.rad, inter_phase_center.dec.rad, 9, 9)
	## calculate shift
	new_pos = inter_phase_center_rad.shift(-offset[0][0], offset[0][1])
	new_pos.rn = 15
	new_pos.dn = 15
	new_pos_str = "%s" % (new_pos)
	
	## correct for potential 2pi rotation
	new_ra = new_pos.ra
	if new_ra > np.pi:
        	new_ra -= 2.0 * np.pi

	## create new coordinate object
	new_coord = SkyCoord(new_ra, new_pos.dec, unit = 'rad', frame = 'icrs')

	## write to open file
	writeStr = '%s: %s\n' % (ms_file.split('/')[-1], new_coord.to_string('hmsdms'))
	f.write(writeStr)
f.close()
