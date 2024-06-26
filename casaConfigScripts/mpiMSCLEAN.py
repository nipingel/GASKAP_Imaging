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
parser.add_argument('-b', '--skipBeam', help ='<optional> list of beams to skip', nargs = '+')
parser.add_argument('-i', '--skipInter', help = '<optional> list of interleaves to skip', nargs = '+')
parser.add_argument('-l', '--chanNum', help='<optional> channel number if dealing with split ms files')
args, unknown = parser.parse_known_args()

## unpack/reformat input to lists for generating visibility list
skipBeamList = args.skipBeam
skipInterList = args.skipInter

## unpack required imaging arguments
totNiter = int(args.totNiter)
nCycleNiter = int(args.nCycleNiter)
minorThresh = int(args.minorThresh)
phaseCenterStr = args.phaseCenter[0]
outputName = args.output
inputRestart = args.restart

## generate visibility list with input arguments
sys.argv = ['../utils/genVisList.py', '-s', args.startBeam, '-e', args.endBeam, '-d', args.subDir, '-b', skipBeamList, '-i', skipInterList, '-c', args.chanNum]
#execfile('../utils/genVisList.py', globals())
execfile('../utils/genVisList.py')
#visList = ['/avatar/nipingel/ASKAP/SMC/data/pilot_obs/ms_data/10941_10944/GASKAP_M344-11B_T0-0A/CONTSUB/scienceData_SB10941_SB10944_GASKAP_M344-11B_T0-0A.beam05_SL.binned.contsub_chan225.ms', '/avatar/nipingel/ASKAP/SMC/data/pilot_obs/ms_data/10941_10944/GASKAP_M344-11B_T0-0A/CONTSUB/scienceData_SB10941_SB10944_GASKAP_M344-11B_T0-0A.beam00_SL.binned.contsub_chan225.ms']

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
outframe = 'LSRK'
restfreq = '1.420405GHz'
#restfreq = []
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
#vptable = '../misc/ASKAP_Holo.tab'
#vptable = '../misc/ASKAP_11mdiam_1mblockage.tab'
gridder='mosaic'
#wprojplanes=1024
#psterm = True
#aterm = False
#wbawp = False
mosweight=False
usepointing=False

## deconvolution parameters ##
deconvolver = 'multiscale'
#scales = [0, 4, 8, 16, 32] # point source, ~2xbeam, ..., scale at which msclean does not diverge 
scales = [0, 4, 8]
smallscalebias = 0.4
niter = totNiter
cycleniter=nCycleNiter
cyclefactor = 1.0 ## set < 1.0 to clean deeper before triggering major cycle
minpsffraction = 0.05 ## clean deeper before triggering major cycle
maxpsffraction = 0.8 ## keep default cleaning depth per minor cycle (clean at least the top 20%)
threshold = '%dmJy' % minorThresh
restoringbeam = '30.0arcsec'
pblimit = 0.05
normtype = 'flatnoise'

## visibility weighting ##
#weighting = 'natural'
weighting = 'briggs'
robust = 1.1

## additional parameters
interactive = False
verbose = True
parallel = True
calcpsf=True
calcres=True
restart = False

## check if we are restarting
if inputRestart == 'True':
	calcpsf = False
	calcres = False
	restart = True
#tclean()
tclean(vis = visList, imagename = imagename, selectdata = True, datacolumn = datacolumn, phasecenter = phasecenter, imsize = imsize, cell = cell, antenna = antenna, 
	specmode = specmode, outframe = outframe, restfreq = restfreq, usemask = usemask, mask = mask, interpolation = interpolation, vptable = vptable, gridder = gridder, 
	mosweight = mosweight, scales = scales, usepointing = usepointing, deconvolver = deconvolver, niter = niter, cycleniter = cycleniter, cyclefactor = 0.75, threshold = threshold, 
	restoringbeam = restoringbeam, pblimit = pblimit, normtype = normtype, weighting = weighting, interactive = False, calcpsf = calcpsf, calcres = calcres, 
	parallel = parallel, restart = restart)
