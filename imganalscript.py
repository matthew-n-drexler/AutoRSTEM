# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 14:04:23 2019

@author: shini
"""

import fftcompression
import rsicompression
import sandwhichsmooth
import levelgraph
import pointfitting
import lonelattice
import latticeanalysis
import numpy
import imageio
import matplotlib.pyplot as mpl

flname = input('Please enter the name of your file: ')
[fname, ftype] = flname.split('.')
if ftype == 'csv':
    imgdat = numpy.genfromtxt(flname, delimiter = ',')
else:
    imgdat = imageio.imread(flname)
imprad = fftcompression.findcompressionradius(imgdat)
smthed = sandwhichsmooth.cycleinterp(imgdat, imprad)

iddimg = rsicompression.imageevaluation(smthed, imprad)
atmpos = rsicompression.pointdetection(iddimg, imprad)
lonlat = lonelattice.lonelattice()
lonlat.djkbuild(atmpos)
preref = lonlat.disply(imgdat.shape)
lonlat.refinepoints(smthed)
lonlat.redjkbuild()
posref = lonlat.disply(imgdat.shape)
lonlat.heightest(imgdat)
hgtfit = pointfitting.emforsize(lonlat.heightstat(), 30)
lonlat.catheight(hgtfit)
edgsts = lonlat.edgrep()
proces = latticeanalysis.strainanalysis(edgsts, orientation = True, category = True, position = True)
numpy.savetxt(f'{fname}_edge_list.csv', edgsts, delimiter = ',')
numpy.savetxt(f'{fname}_length_height.csv', proces, delimiter = ',')
mpl.figure()
mpl.imshow(imgdat)
mpl.figure()
mpl.imshow(smthed)
mpl.figure()
mpl.imshow(rsicompression.visualizecategoryimage(iddimg))
mpl.figure()
mpl.imshow(rsicompression.markpositions(imgdat, atmpos))
mpl.figure()
mpl.imshow(lonlat.disply(imgdat.shape))
mpl.figure()
mpl.imshow(preref)
mpl.figure()
mpl.imshow(posref)