
## image/output parameters
visList = []
execfile('genVisList_chansub.py')
default('tclean')
vis = visList
imagename = 'newcasatest'
selectdata = True
datacolumn = 'corrected'
phasecenter = 'J2000 00h52m44s -72d49m42s'
imsize = [5000, 5000]
cell = ['7arcsec', '7arcsec']

## data selection parameters
specmode = 'cube'
#start = '1419.611MHz'
#width = '18.519kHz'
nchan = 24
#chanchunks = 12
outframe = 'LSRK'
restfreq = '1.420405GHz'

## gridding/deconvolution parameters
interpolation = 'linear'
gridder ='mosaic'
vptable = 'ASKAP_AIRY_BP.tab'
usepointing = False
mosweight = False
deconvolver = 'multiscale'
scales = [0, 5, 10, 25, 50]
smallscalebias = 0.6
restoringbeam = []
pblimit = 0.1
normtype = 'flatnoise'
dogrowprune = False
weighting = 'briggs'
robust = 1.1
niter = 15000
cycleniter=5000
threshold = '5mJy'
interactive = False
verbose = True
parallel = True
calcpsf=False

field='0'

tclean()
