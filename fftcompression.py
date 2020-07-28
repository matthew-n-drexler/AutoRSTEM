# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:31:07 2020

@author: shini
"""

import numpy
#import imageio
import scipy.interpolate as interp
#import scipy.optimize as sciopt
import matplotlib.pyplot as mpl
#from mpl_toolkits.mplot3d import Axes3D

def doublegaussian(pos, xone, hone, sone, xtwo, htwo, stwo):
    return hone * numpy.exp(-1 * (pos - xone)**2 / (2 * sone**2)) + htwo * numpy.exp(-1 * (pos - xtwo)**2 / (2 * stwo**2))

def findcompressionradius(stemimage, noisy = False):
    # Find the FFT of the original image and turn it into a human-readable 
    # format
    stemfft = numpy.fft.fft2(stemimage)**2
    stemfft = numpy.log10((numpy.real(stemfft)**2 + numpy.imag(stemfft)**2)**.5)
    rearfft = numpy.zeros(stemfft.shape)
    rearfft[:, 0:int(rearfft.shape[1] / 2)] = stemfft[:, int(rearfft.shape[1] / 2):rearfft.shape[1]]
    rearfft[:, int(rearfft.shape[1] / 2):rearfft.shape[1]] = stemfft[:, 0:int(rearfft.shape[1] / 2)]
    stemfft[0:int(rearfft.shape[0] / 2), :] = rearfft[int(rearfft.shape[0] / 2):rearfft.shape[0], :]
    stemfft[int(rearfft.shape[0] / 2):rearfft.shape[0], :] = rearfft[0:int(rearfft.shape[0] / 2), :]
    if noisy:
        mpl.figure()
        mpl.imshow(stemfft)
    # Get the radial intensity profile of the 
    centerpoint = numpy.array([int(stemfft.shape[0] / 2), int(stemfft.shape[1] / 2)])
    intensityprofile = numpy.zeros((int(numpy.ceil(((stemfft.shape[0] / 2)**2 + (stemfft.shape[1] / 2)**2)**.5) + 1), 2))
    for i in range(stemfft.shape[0]):
        for j in range(stemfft.shape[1]):
            actualdistance = ((i - centerpoint[0])**2 + (j - centerpoint[1])**2)**.5
            lowerguidepointpercent = 1 - (actualdistance - numpy.floor(actualdistance))
            intensityprofile[int(actualdistance)][0] = intensityprofile[int(actualdistance)][0] + stemfft[i][j] * lowerguidepointpercent
            intensityprofile[int(actualdistance)][1] = intensityprofile[int(actualdistance)][1] + lowerguidepointpercent
            intensityprofile[int(actualdistance) + 1][0] = intensityprofile[int(actualdistance) + 1][0] + stemfft[i][j] * (1 - lowerguidepointpercent)
            intensityprofile[int(actualdistance) + 1][1] = intensityprofile[int(actualdistance) + 1][1] + (1 - lowerguidepointpercent)
    intensityprofile[:, 0] = intensityprofile[:, 0] / intensityprofile[:, 1]
    # Find the minimum radius that contains all diffraction points. This can 
    # be done by sorting the intensity profile and forming a Lorenz curve, 
    # then finding the two rectangles contained within the curve with the 
    # highest area. 
    sortedradius = numpy.sort(intensityprofile[:, 0])
    lorenzcurve = numpy.zeros(intensityprofile.shape)
    for i in range(sortedradius.shape[0]):
        lorenzcurve[i][0] = sortedradius[i]
        lorenzcurve[i][1] = (i + 1) / sortedradius.shape[0]
    interpolatedx = numpy.arange(sortedradius[0], sortedradius[sortedradius.shape[0] - 1], .01)
    interpolatedy = interp.griddata((lorenzcurve[:, 0]), (lorenzcurve[:,1]), interpolatedx)
    bigarea = 0
    combop = [0, 1]
    for i in range(1, interpolatedx.shape[0] - 2):
        for j in range(2, interpolatedx.shape[0] - 1):
            area = (interpolatedy[i] - numpy.min(interpolatedy)) * (interpolatedx[interpolatedx.shape[0] - 1] - interpolatedx[i]) + (interpolatedy[j] - interpolatedy[i]) * (interpolatedx[interpolatedx.shape[0] - 1] - interpolatedx[j])
            if area > bigarea:
                combop = [i, j]
                bigarea = area
    # Determining the correct radius is difficult. You can't just use the 
    # highest x-value with a y-value greater than the value, so you need to 
    # find the point with the lowest value that has the most number of points 
    # greater than the threshold below it and less than the threshold above it
    if noisy:
        print([[interpolatedx[combop[0]], interpolatedy[combop[0]]], [interpolatedx[combop[1]], interpolatedy[combop[1]]]])
    threshold = interpolatedx[combop[0]]
    #threshold = numpy.sum(stemfft) / (stemfft.shape[0] * stemfft.shape[1])
    numberhigher = 0
    numberlower = 0
    for i in range(intensityprofile.shape[0]):
        if intensityprofile[i][0] > threshold:
            numberhigher = numberhigher + 1
        else:
            numberlower = numberlower + 1
    scorearray = numpy.zeros((intensityprofile.shape[0]))
    highcount = 0
    lowcount = numberlower
    highscore = 0
    for i in range(intensityprofile.shape[0]):
        if intensityprofile[i][0] > threshold:
            highcount = highcount + 1
        else:
            lowcount = lowcount - 1
        scorearray[i] = highcount / (i + 1) + lowcount / (intensityprofile.shape[0] - i)
        if scorearray[i] > scorearray[highscore]:
            highscore = i
    compressionfactor = highscore / (stemimage.shape[0] / 2)
    if noisy:
        print(compressionfactor**-1)
        mpl.figure()
        mpl.scatter(range(intensityprofile.shape[0]), intensityprofile[:, 0])
        mpl.scatter(range(intensityprofile.shape[0]), scorearray)
        mpl.plot(range(intensityprofile.shape[0]), threshold * numpy.ones((intensityprofile.shape[0])))
        mpl.figure()
        mpl.scatter(interpolatedx, interpolatedy)
    return int(numpy.ceil(compressionfactor**-1))

def findaveragefftintensity(stemimage):
    # Find the FFT of the original image and turn it into a human-readable 
    # format
    stemfft = numpy.fft.fft2(stemimage)**2
    stemfft = numpy.log10((numpy.real(stemfft)**2 + numpy.imag(stemfft)**2)**.5)
    rearfft = numpy.zeros(stemfft.shape)
    rearfft[:, 0:int(rearfft.shape[1] / 2)] = stemfft[:, int(rearfft.shape[1] / 2):rearfft.shape[1]]
    rearfft[:, int(rearfft.shape[1] / 2):rearfft.shape[1]] = stemfft[:, 0:int(rearfft.shape[1] / 2)]
    stemfft[0:int(rearfft.shape[0] / 2), :] = rearfft[int(rearfft.shape[0] / 2):rearfft.shape[0], :]
    stemfft[int(rearfft.shape[0] / 2):rearfft.shape[0], :] = rearfft[0:int(rearfft.shape[0] / 2), :]
    averageintensity = numpy.sum(stemfft) / (stemfft.shape[0] * stemfft.shape[1])
    print(averageintensity)

if __name__ == "__main__":
    flname = input('Please enter the name of your file: ')
    [fname, ftype] = flname.split('.')
    orgimg = numpy.genfromtxt(flname, delimiter = ',')
    schrad = findcompressionradius(orgimg, noisy = True)
    # The way I see it, there are two methods: for each local maxima, find the 
    # decay function and determine if I(x) > I(x+1) for x up to schrad and compare 
    # scores for each point, or for each maxima, see if there is another, higher 
    # maxima less than schrad apart. Neither will be perfect. Can I combine them?
    # The second one first (easier to implement)
# =============================================================================
#     pntimg = numpy.zeros(orgimg.shape)
#     for j in range(orgimg.shape[0]):
#         for i in range(orgimg.shape[1]):
#             isbigg = True
#             if j > 0:
#                 if orgimg[j - 1][i] > orgimg[j][i]:
#                     isbigg = False
#             if i > 0:
#                 if orgimg[j][i - 1] > orgimg[j][i]:
#                     isbigg = False
#             if j < orgimg.shape[0] - 1:
#                 if orgimg[j + 1][i] > orgimg[j][i]:
#                     isbigg = False
#             if i < orgimg.shape[1] - 1:
#                 if orgimg[j][i + 1] > orgimg[j][i]:
#                     isbigg = False
#             if isbigg:
#                 for l in range(int(numpy.max([0, j - schrad])), int(numpy.min([orgimg.shape[0], j + schrad + 1]))):
#                     for k in range(int(numpy.max([0, i - numpy.ceil((schrad**2 - (j - l)**2)**.5)])), int(numpy.min([orgimg.shape[1], i + numpy.ceil((schrad**2 - (j - l)**2)**.5) + 1]))):
#                         if orgimg[j][i] < orgimg[l][k]:
#                             isbigg = False
#             if isbigg:
#                 pntimg[j][i] = 1
#     vizimg = numpy.zeros((orgimg.shape[0], orgimg.shape[1], 3))
#     vizimg[:, :, 0] = (orgimg - numpy.min(orgimg)) / (numpy.max(orgimg) - numpy.min(orgimg))
#     vizimg[:, :, 1] = pntimg
# =============================================================================
    mpl.figure()
    mpl.imshow(orgimg)
    #mpl.figure()
    #mpl.imshow(vizimg)