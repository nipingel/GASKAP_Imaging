"""
8/3/2022
Split out a user provided channel range from input ms file
User inputs:
-p --path - <required> path of ms file
-s --start_chan - <required> starting channel for splitting
-e --end_chan - <required> ending channel for splliting
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to measurement set', required = True)
parser.add_argument('-s', '--start_chan', help='<required> starting channel for splitting', required = True, type = int)
parser.add_argument('-e', '--end_chan', help='<required> ending channel for splitting', required = True, type = int)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## get starting and ending channels
start_chan = args.start_chan
end_chan = args.end_chan

def main():

	## create list of file names
	output_vis_list = []
	for i in range(start_chan, end_chan+1):
		output_vis_list.append('%s_chan%d' % (ms_path, i))

	cnt = 0
	for i in range(start_chan, end_chan+1):
		## set split parameters and run
		vis_name = ms_path
		output_vis = output_vis_list[cnt]
		spw_str='0:%d' % i
		datacolumn_name = 'data'
		cnt+=1
		split(vis = vis_name, outputvis = output_vis, spw=spw_str, datacolumn=datacolumn_name)
if __name__=='__main__':
	main()
	exit()