"""
11/20/2019
Split out a user provided channel fromj input ms file
User inputs:
-p --path - <required> path of ms file
-n --name - <required> name of measurement set
-s --start_chan - <required> starting channel for splitting
-e --end_chan - <required> ending channel for splliting
__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to measurement set', required = True)
parser.add_argument('-n', '--name', help='<required> name of measurement set', required = True)
parser.add_argument('-s', '--start_chan', help='<required> starting channel for splitting', required = True, type = int)
parser.add_argument('-e', '--end_chan', help='<required> ending channel for splitting', required = True, type = int)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## get name of measurement set
ms_name = args.name 

## get starting and ending channels
start_chan = args.start_chan
end_chan = args.end_chan

## create list of file names
output_vis_list = []
for i in range(start_chan, end_chan):
	output_vis_list.append('%s/%s_chan%d' % (path, name, i))

cnt = 0
for i in range(start_chan, end_chan+1):
	## set split parameters and run
	default('split')
	vis = '%s/%s' % (ms_path, ms_name)
	outputvis = output_vis_list[cnt]
	spw='0:%d' % i
	datacolumn = 'data'
	cnt+=1
	split()
