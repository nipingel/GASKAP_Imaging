"""
12/10/2019
Script to set up imaging for a single velocity plane of ASKAP data on Avatar. The control of the script is based on user inputs from 
a PBS script. The user can choose the total number of iterations (if niter == 0, then a dirty image, psf, and initial residual will be made), 
whether to restart from previous images, minor cycle iterations, threshold, phasecenter, start beam, end beam, sub directory (for data location), p
potential beams/interleaves to skip, channel number, and output name. 
 Potential user inputs:
-t --totNiter - <required> total number of iterations
-n --nCycleNiter - <required> total number of minor cycle iterations
-w --minorThresh - <required> minor cycle threshold [mJy]
-p --phaseCenter - <required> phase center of image (e.g., 'J2000 00h52m44s -72d49m42')
-d --subDir - <required> sub-directory to look for ms files (e.g., BINNED)
-o --output - <required> output name
-s --startBeam - <optional> If only a subset of beams are required, the user can provide starting & ending beam numbers 
-e --endBeam - <optional>ending beam 
-b --skipBeam - <optional> list of beams to skip
-i --skipIter - <optional> list of interleaves to skip'
-c --chanNum - <optional> channel number if dealing with split ms files 

__author__="Nickolas Pingel"
__version__="1.0"
__email__="Nickolas.Pingel@anu.edu.au"
__status__="Production"
"""
## imports
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--totNiter', help = '<required> total number of iterations', required = True)
parser.add_argument('-n', '--nCycleNiter', help = '<required> total number of minor cycle iterations', required = True)
parser.add_argument('-w', '--minorThresh', help = '<required> minor cycle threshold [mJy]', required = True)
parser.add_argument('-p', '--phaseCenter', help = '<required> phase center of image (e.g., \'J2000 00h52m44s -72d49m42\')', required = True, nargs='+')
parser.add_argument('-d', '--subDir', help = '<required> sub-directory to look for files', required = True)
parser.add_argument('-o', '--output', help = '<required> output name', required = True)
parser.add_argument('-r', '--restart', help = '<optional> restart from previously generated images')
parser.add_argument('-s', '--startBeam', help ='<optional> starting beam', default = 0)
parser.add_argument('-e', '--endBeam', help = '<optional> ending beam', default = 35)
parser.add_argument('-b', '--skipBeam', help ='<optional> list of beams to skip')
parser.add_argument('-i', '--skipInter', help = '<optional> list of interleaves to skip')
parser.add_argument('-l', '--chanNum', help='<optional> channel number if dealing with split ms files')
args, unknown = parser.parse_known_args()
print(args)
## unpack/reformat input to lists for generating visibility list
skipBeamList = [args.skipBeam]
skipInterList = [args.skipInter]

## unpack required imaging arguments
totNiter = int(args.totNiter)
nCycleNiter = int(args.nCycleNiter)
minorThresh = int(args.minorThresh)
phaseCenterStr = args.phaseCenter[0]
outputName = args.output
restart = args.restart

## generate visibility list with input arguments
sys.argv = ['../utils/genVisList.py', '-s', args.startBeam, '-e', args.endBeam, '-d', args.subDir, '-b', args.skipBeam, '-i', args.skipInter, '-c', args.chanNum]
execfile('../utils/genVisList.py')
print(visList)

## image/output parameters
default('tclean')

vis = visList
imagename = outputName
selectdata = True
datacolumn = 'data'
phasecenter = phaseCenterStr
imsize = [5000, 5000]
cell = ['7arcsec', '7arcsec']

## data selection parameters
specmode = 'mfs'
outframe = 'LSRK'
restfreq = '1.420405GHz'

## mask parameters
usemask = 'auto-multithresh'
pbmask = 0.2
sidelobethreshold = 2.5
noisethreshold = 4.25
minbeamfrac = 0.3
lownoisethreshold = 1.5
negativethreshold = 2.5
verbose = True

## gridding/deconvolution parameters
interpolation = 'linear'
gridder ='mosaic'
vptable = '../misc/ASKAP_AIRY_BP.tab'
usepointing = False
mosweight = False
deconvolver = 'multiscale'
scales = [0, 5, 10, 25, 50]
smallscalebias = 0.6
restoringbeam = []
pblimit = 0.05
normtype = 'flatnoise'
dogrowprune = False

## visibility weighting
weighting = 'briggs'
robust = 1.1

## deconvolution parameters
niter = totNiter
cycleniter=nCycleNiter
threshold = '%dmJy' % minorThresh
interactive = False
verbose = True
parallel = True

## check if we are restarting
if restart is not None:
	calcpsf = False
	calcres = False
	restart = True
inp
#tclean()
