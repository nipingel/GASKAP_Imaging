"""
7/22/2020
Script to set up imaging for a single beam for GASKAP OH observations. The control of the script is based on user inputs from 
a PBS script. The user can choose the total number of iterations (if niter == 0, then a dirty image, psf, and initial residual will be made), 
whether to restart from previous images, minor cycle iterations, threshold, sub directory (for data location), and output name. 
 Potential user inputs:
-t --totNiter - <required> total number of iterations
-n --nCycleNiter - <required> total number of minor cycle iterations
-w --minorThresh - <required> minor cycle threshold [mJy]
-o --output - <required> output name
-f --restfreq - <required> rest frequency of OH transition we're imaging in units of GHz
-r --restart - <optional> restart from previously generated images

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
parser.add_argument('-v', '--visPath', help = '<required> FULL path to measurement set for beam'  = True)
parser.add_argument('-o', '--output', help = '<required> output name', required = True)
parser.add_argument('-f', '--restfreq', help = '<required> rest frequency of OH transition we\'re imaging in units of GHz')
parser.add_argument('-r', '--restart', help = '<optional> restart from previously generated images', default = False)
args, unknown = parser.parse_known_args()

## unpack/reformat input to lists for generating visibility list
skipBeamList = [args.skipBeam]
skipInterList = [args.skipInter]

## unpack required imaging arguments
totNiter = int(args.totNiter)
nCycleNiter = int(args.nCycleNiter)
minorThresh = int(args.minorThresh)
inputVis = args.visPath
outputName = args.output
restfreq = args.restfreq
inputRestart = args.restart

## image/output parameters
default('tclean')

vis = inputVis
imagename = outputName
selectdata = True
datacolumn = 'data'
imsize = [800, 800]
cell = ['7arcsec', '7arcsec']

## data selection parameters
specmode = 'cube'
outframe = 'TOPO'
restfreq = '%sGHz' % restfreq

## manual mask parameters
usemask = 'user'
mask = ''

## automasking parameters ##
#usemask = 'auto-multithresh'
#pbmask = 0.5
#sidelobethreshold = 2.5
#noisethreshold = 3.5
#minbeamfrac = 0.3
#lownoisethreshold = 1.75
#negativethreshold = 0.0
#growiterations=75
#dogrowprune=False
#verbose = True

## gridding parameters ##
interpolation = 'linear'
vptable = '../misc/ASKAP_AIRY_BP.tab'
gridder='mosaic'
#wprojplanes=1024
#psterm = True
#aterm = False
#wbawp = False
mosweight=False
usepointing=False

## deconvolution parameters ##
deconvolver = 'multiscale'
scales = [0, 4, 8] # point source, ~2xbeam, ..., scale at which msclean does not diverge 
smallscalebias = 0.4
niter = totNiter
cycleniter=nCycleNiter
cyclefactor = 0.5 ## set < 1.0 to clean deeper before triggering major cycle
minpsffraction = 0.05 ## clean deeper before triggering major cycle
maxpsffraction = 0.8 ## keep default cleaning depth per minor cycle (clean at least the top 20%)
threshold = '%dmJy' % minorThresh
restoringbeam = '30.0arcsec'
pblimit = 0.05
normtype = 'flatnoise'

## visibility weighting ##
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
