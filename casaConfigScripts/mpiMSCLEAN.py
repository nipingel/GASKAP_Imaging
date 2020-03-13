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
parser.add_argument('-r', '--restart', help = '<optional> restart from previously generated images', default = False)
parser.add_argument('-s', '--startBeam', help ='<optional> starting beam', default = 0)
parser.add_argument('-e', '--endBeam', help = '<optional> ending beam', default = 35)
parser.add_argument('-b', '--skipBeam', help ='<optional> list of beams to skip')
parser.add_argument('-i', '--skipInter', help = '<optional> list of interleaves to skip')
parser.add_argument('-l', '--chanNum', help='<optional> channel number if dealing with split ms files')
args, unknown = parser.parse_known_args()

## unpack/reformat input to lists for generating visibility list
skipBeamList = [args.skipBeam]
skipInterList = [args.skipInter]

## unpack required imaging arguments
totNiter = int(args.totNiter)
nCycleNiter = int(args.nCycleNiter)
minorThresh = int(args.minorThresh)
phaseCenterStr = args.phaseCenter[0]
outputName = args.output
inputRestart = args.restart

## generate visibility list with input arguments
sys.argv = ['../utils/genVisList.py', '-s', args.startBeam, '-e', args.endBeam, '-d', args.subDir, '-b', skipBeamList, '-i', skipInterList, '-c', args.chanNum]
execfile('../utils/genVisList.py')

## image/output parameters
default('tclean')

vis = visList
imagename = outputName
selectdata = True
datacolumn = 'data'
phasecenter = phaseCenterStr
imsize = [4300, 4300]
cell = ['7arcsec', '7arcsec']

## data selection parameters
specmode = 'mfs'
outframe = 'TOPO'
restfreq = '1.420405GHz'

## mask parameters
usemask = 'auto-multithresh'
pbmask = 0.85
sidelobethreshold = 3.0
noisethreshold = 4.25
minbeamfrac = 0.3
lownoisethreshold = 2.0
negativethreshold = 0.0
growiterations=75
verbose = True

## gridding/deconvolution parameters
interpolation = 'linear'
vptable = '../misc/ASKAP_AIRY_BP.tab'
gridder='mosaic'
#wprojplanes=1024
#psterm = True
#aterm = False
#wbawp = False
mosweight=False
usepointing=False

deconvolver = 'multiscale'
#scales = [0, 5, 15, 45, 135, 250] ## maximum recoverable scale based on minimum baseline: 280 pixels => 32.8 arcmin
scales = [0, 8, 16, 32]
smallscalebias = 0.6
niter = totNiter
cycleniter=nCycleNiter
cyclefactor = 0.25 ## set < 1.0 to clean deeper before triggering major cycle
minpsffraction = 0.025 ## clean deeper before triggering major cycle
maxpsffraction = 0.8 ## keep default cleaning depth per minor cycle (clean at least the top 20%)
threshold = '%dmJy' % minorThresh
restoringbeam = []
pblimit = 0.05
normtype = 'flatnoise'
dogrowprune = False

## visibility weighting
weighting = 'briggs'
robust = 1.1

## additional parameters
interactive = False
verbose = True
parallel = True
calcpsf=True
calcres=True

## check if we are restarting
if inputRestart == 'True':
	calcpsf = False
	calcres = False
	restart = True
tclean()
