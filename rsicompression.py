# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 11:08:18 2020

@author: shini
"""

import numpy
import matplotlib.pyplot as mpl

def imageevaluation(image, radius):
    categi = numpy.zeros((image.shape[0], image.shape[1], 3))
    #viwwin = numpy.zeros((2 * comprd + 1, 2 * comprd + 1))
    # No feature
    catega = numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # Edge
    categb = numpy.array([[[1, 1, 1], [1, 1, 1], [.4, .4, .4]], [[1, 1, 1], [1, 1, .4], [1, .4, .4]], [[1, 1, .4], [1, 1, .4], [1, 1, .4]], [[1, .4, .4], [1, 1, .4], [1, 1, 1]], [[.4, .4, .4], [1, 1, 1], [1, 1, 1]], [[.4, .4, 1], [.4, 1, 1], [1, 1, 1]], [[.4, 1, 1], [.4, 1, 1], [.4, 1, 1]], [[1, 1, 1], [.4, 1, 1], [.4, .4, 1]]])
    # Ridge
    categc = numpy.array([[[.4, .4, .4], [1, 1, 1], [.4, .4, .4]], [[.4, .4, 1], [.4, 1, .4], [1, .4, .4]], [[.4, 1, .4], [.4, 1, .4], [.4, 1, .4]], [[1, .4, .4], [.4, 1, .4], [.4, .4, 1]]])
    # Peninsula
    categd = numpy.array([[[1, 1, 1], [.4, 1, .4], [.4, .4, .4]], [[1, 1, .4], [1, 1, .4], [.4, .4, .4]], [[1, .4, .4], [1, 1, .4], [1, .4, .4]], [[.4, .4, .4], [1, 1, .4], [1, 1, .4]], [[.4, .4, .4], [.4, 1, .4], [1, 1, 1]], [[.4, .4, .4], [.4, 1, 1], [.4, 1, 1]], [[.4, .4, 1], [.4, 1, 1], [.4, .4, 1]], [[.4, 1, 1], [.4, 1, 1], [.4, .4, .4]]])
    # Peak
    catege = numpy.array([[.4, .4, .4], [.4, 1, .4], [.4, .4, .4]])
    #j = int(orgimg.shape[0] * numpy.random.rand())
    #i = int(orgimg.shape[1] * numpy.random.rand())
    #print([i, j])
    for j in range(image.shape[0]):
        for i in range(image.shape[1]):
            compix = numpy.zeros((3, 3, 2))
            for l in range(int(numpy.max([0, j - radius])), int(numpy.min([image.shape[0], j + radius + 1]))):
                if j == l:
                    highx = radius
                else:
                    highx = int(numpy.round((radius**2 - (numpy.abs(j - l) - .5)**2)**.5))
                for k in range(int(numpy.max([0, i - highx])), int(numpy.min([image.shape[1], i + highx + 1]))):
                    #viwwin[comprd - (j - l)][comprd - (i - k)] = orgimg[l][k]
                    mnrdst = ((i - k)**2 + (j - l)**2)**.5
                    if mnrdst <= radius / 2:
                        compix[1][1][0] = compix[1][1][0] + image[l][k]
                        compix[1][1][1] = compix[1][1][1] + 1
                    if mnrdst >= radius / 2:
                        pntsin = (l - j) / mnrdst
                        pntcos = (k - i) / mnrdst
                        if pntcos == 1: # Border of sectors (1, 0) and (2, 0)
                            compix[0][2][0] = compix[0][2][0] + image[l][k]
                            compix[1][2][0] = compix[1][2][0] + image[l][k]
                            compix[2][2][0] = compix[2][2][0] + image[l][k]
                            compix[0][2][1] = compix[0][2][1] + 1
                            compix[1][2][1] = compix[1][2][1] + 1
                            compix[2][2][1] = compix[2][2][1] + 1
                        elif pntcos > 1 / 2**.5:
                            if pntsin > 0: # Sector (1, 0)
                                compix[1][2][0] = compix[1][2][0] + image[l][k]
                                compix[2][2][0] = compix[2][2][0] + image[l][k]
                                compix[1][2][1] = compix[1][2][1] + 1
                                compix[2][2][1] = compix[2][2][1] + 1
                            else: # Sector (2, 0)
                                compix[1][2][0] = compix[1][2][0] + image[l][k]
                                compix[0][2][0] = compix[0][2][0] + image[l][k]
                                compix[1][2][1] = compix[1][2][1] + 1
                                compix[0][2][1] = compix[0][2][1] + 1
                        elif pntcos == 1 / 2**.5:
                            if pntsin > 0: # Border of sectors (0, 1) and (1, 0)
                                compix[1][2][0] = compix[1][2][0] + image[l][k]
                                compix[2][2][0] = compix[2][2][0] + image[l][k]
                                compix[2][1][0] = compix[2][1][0] + image[l][k]
                                compix[1][2][1] = compix[1][2][1] + 1
                                compix[2][2][1] = compix[2][2][1] + 1
                                compix[2][1][1] = compix[2][1][1] + 1
                            else: # Border of sectors (3, 1) and (2, 0)
                                compix[1][2][0] = compix[1][2][0] + image[l][k]
                                compix[0][2][0] = compix[0][2][0] + image[l][k]
                                compix[0][1][0] = compix[0][1][0] + image[l][k]
                                compix[1][2][1] = compix[1][2][1] + 1
                                compix[0][2][1] = compix[0][2][1] + 1
                                compix[0][1][1] = compix[0][1][1] + 1
                        elif pntcos > 0:
                            if pntsin > 0: # Sector (0, 1)
                                compix[2][2][0] = compix[2][2][0] + image[l][k]
                                compix[2][1][0] = compix[2][1][0] + image[l][k]
                                compix[2][2][1] = compix[2][2][1] + 1
                                compix[2][1][1] = compix[2][1][1] + 1
                            else: # Sector (3, 1)
                                compix[0][2][0] = compix[0][2][0] + image[l][k]
                                compix[0][1][0] = compix[0][1][0] + image[l][k]
                                compix[0][2][1] = compix[0][2][1] + 1
                                compix[0][1][1] = compix[0][1][1] + 1
                        elif pntcos == 0:
                            if pntsin > 0: # Border of sectors (0, 1) and (0, 2)
                                compix[2][2][0] = compix[2][2][0] + image[l][k]
                                compix[2][1][0] = compix[2][1][0] + image[l][k]
                                compix[2][0][0] = compix[2][0][0] + image[l][k]
                                compix[2][2][1] = compix[2][2][1] + 1
                                compix[2][1][1] = compix[2][1][1] + 1
                                compix[2][0][1] = compix[2][0][1] + 1
                            else: # Border of sectors (3, 1) and (3, 2)
                                compix[0][2][0] = compix[0][2][0] + image[l][k]
                                compix[0][1][0] = compix[0][1][0] + image[l][k]
                                compix[0][0][0] = compix[0][0][0] + image[l][k]
                                compix[0][2][1] = compix[0][2][1] + 1
                                compix[0][1][1] = compix[0][1][1] + 1
                                compix[0][0][1] = compix[0][0][1] + 1
                        elif pntcos > -1 / 2**.5:
                            if pntsin > 0: # Sector (0, 2)
                                compix[2][1][0] = compix[2][1][0] + image[l][k]
                                compix[2][0][0] = compix[2][0][0] + image[l][k]
                                compix[2][1][1] = compix[2][1][1] + 1
                                compix[2][0][1] = compix[2][0][1] + 1
                            else: # Sector (3, 2)
                                compix[0][1][0] = compix[0][1][0] + image[l][k]
                                compix[0][0][0] = compix[0][0][0] + image[l][k]
                                compix[0][1][1] = compix[0][1][1] + 1
                                compix[0][0][1] = compix[0][0][1] + 1
                        elif pntcos == -1 / 2**.5:
                            if pntsin > 0: # Border of sectors (0, 2) and (1, 3)
                                compix[2][1][0] = compix[2][1][0] + image[l][k]
                                compix[2][0][0] = compix[2][0][0] + image[l][k]
                                compix[1][0][0] = compix[1][0][0] + image[l][k]
                                compix[2][1][1] = compix[2][1][1] + 1
                                compix[2][0][1] = compix[2][0][1] + 1
                                compix[1][0][1] = compix[1][0][1] + 1
                            else: # Border of sectors (3, 2) and (2, 3)
                                compix[0][1][0] = compix[0][1][0] + image[l][k]
                                compix[0][0][0] = compix[0][0][0] + image[l][k]
                                compix[1][0][0] = compix[1][0][0] + image[l][k]
                                compix[0][1][1] = compix[0][1][1] + 1
                                compix[0][0][1] = compix[0][0][1] + 1
                                compix[1][0][1] = compix[1][0][1] + 1
                        elif pntcos > -1:
                            if pntsin > 0: # Sector (1, 3)
                                compix[2][0][0] = compix[2][0][0] + image[l][k]
                                compix[1][0][0] = compix[1][0][0] + image[l][k]
                                compix[2][0][1] = compix[2][0][1] + 1
                                compix[1][0][1] = compix[1][0][1] + 1
                            else: # Sector (2, 3)
                                compix[0][0][0] = compix[0][0][0] + image[l][k]
                                compix[1][0][0] = compix[1][0][0] + image[l][k]
                                compix[0][0][1] = compix[0][0][1] + 1
                                compix[1][0][1] = compix[1][0][1] + 1
                        elif pntcos == -1: # Border of sectors (1, 3) and (2, 3)
                            compix[2][0][0] = compix[2][0][0] + image[l][k]
                            compix[1][0][0] = compix[1][0][0] + image[l][k]
                            compix[0][0][0] = compix[0][0][0] + image[l][k]
                            compix[2][0][1] = compix[2][0][1] + 1
                            compix[1][0][1] = compix[1][0][1] + 1
                            compix[0][0][1] = compix[0][0][1] + 1
            minhgt = compix[1][1][0]
            for n in range(compix.shape[0]):
                for m in range(compix.shape[1]):
                    if compix[n][m][1] > 0:
                        compix[n][m][0] = compix[n][m][0] / compix[n][m][1]
                        if compix[n][m][0] < minhgt:
                            minhgt = compix[n][m][0]
            if minhgt == compix[1][1][0]:
                nrmpix = compix[:, :, 0] / minhgt
            else:
                nrmpix = (compix[:, :, 0] - minhgt) / (compix[1][1][0] - minhgt)
            mtchsc = 0
            categ = 0
            for m in range(compix.shape[0]):
                for n in range(compix.shape[1]):
                    if compix[m][n][1] > 0:
                        mtchsc = mtchsc + (nrmpix[m][n] - catega[m][n])**2
            for u in range(categb.shape[0]):
                cscore = 0
                for m in range(compix.shape[0]):
                    for n in range(compix.shape[1]):
                        if compix[m][n][1] > 0:
                            cscore = cscore + (nrmpix[m][n] - categb[u][m][n])**2
                if cscore < mtchsc:
                    categ = 1
                    mtchsc = cscore
            for u in range(categc.shape[0]):
                cscore = 0
                for m in range(compix.shape[0]):
                    for n in range(compix.shape[1]):
                        if compix[m][n][1] > 0:
                            cscore = cscore + (nrmpix[m][n] - categc[u][m][n])**2
                if cscore < mtchsc:
                    categ = 2
                    mtchsc = cscore
            for u in range(categd.shape[0]):
                cscore = 0
                for m in range(compix.shape[0]):
                    for n in range(compix.shape[1]):
                        if compix[m][n][1] > 0:
                            cscore = cscore + (nrmpix[m][n] - categd[u][m][n])**2
                if cscore < mtchsc:
                    categ = 3
                    mtchsc = cscore
            cscore = 0
            for m in range(compix.shape[0]):
                for n in range(compix.shape[1]):
                    if compix[m][n][1] > 0:
                        cscore = cscore + (nrmpix[m][n] - catege[m][n])**2
            if cscore < mtchsc:
                categ = 4
                mtchsc = cscore
            pekscr = [0, 0]
            for n in range(3):
                for m in range(3):
                    if compix[m][n][1] > 0:
                        pekscr[0] = pekscr[0] + (compix[1][1][0] - compix[m][n][0])
                        pekscr[1] = pekscr[1] + 1
            categi[j][i][0] = pekscr[0] / pekscr[1]
            categi[j][i][1] = categ
    return categi

def pointdetection(catimage, radius):
    pointlist = []
    aralst = []
    for l in range(-1 * radius, radius + 1):
        for k in range(-1 * int(numpy.round((radius**2 - (numpy.abs(l) - .5)**2)**.5)), int(numpy.round((radius**2 - (numpy.abs(l) - .5)**2)**.5)) + 1):
            m = 0
            srchng = True
            while m < len(aralst) and srchng:
                if (k**2 + l**2)**.5 <= (aralst[m][0]**2 + aralst[m][1]**2)**.5:
                    srchng = False
                else:
                    m = m + 1
            if srchng:
                aralst.append([k, l])
            else:
                aralst.insert(m, [k, l])
    aralst.pop(0)
    for j in range(catimage.shape[0]):
        for i in range(catimage.shape[1]):
            if catimage[j][i][1] > 0:
                m = 0
                srchng = True
                while m < len(aralst) and srchng:
                    if j + aralst[m][1] >= 0 and j + aralst[m][1] < catimage.shape[0] and i + aralst[m][0] >= 0 and i + aralst[m][0] < catimage.shape[1]:
                        if catimage[j + aralst[m][1]][i + aralst[m][0]][1] > catimage[j][i][1] or (catimage[j + aralst[m][1]][i + aralst[m][0]][0] > catimage[j][i][0] and catimage[j + aralst[m][1]][i + aralst[m][0]][1] == catimage[j][i][1]):
                            srchng = False
                        else:
                            m = m + 1
                    else:
                        m = m + 1
                if srchng:
                    pointlist.append([i, j])
    return pointlist

def visualizecategoryimage(categoryimage):
    outputimage = numpy.zeros(categoryimage.shape)
    scoremax = numpy.max(categoryimage[:, :, 0])
    scoremin = numpy.min(categoryimage[:, :, 0])
    for j in range(categoryimage.shape[0]):
        for i in range(categoryimage.shape[1]):
            outputimage[j][i][0] = (categoryimage[j][i][0] - scoremin) / (scoremax - scoremin)
            outputimage[j][i][1] = categoryimage[j][i][1] / 4
            outputimage[j][i][2] = (4 - categoryimage[j][i][1]) / 4
    return outputimage

def markpositions(image, points):
    markedimage = numpy.ones((image.shape[0], image.shape[1], 3))
    markedimage[:, :, 0] = (image - numpy.min(image)) / (numpy.max(image) - numpy.min(image))
    markedimage[:, :, 1] = (image - numpy.min(image)) / (numpy.max(image) - numpy.min(image))
    markedimage[:, :, 2] = (image - numpy.min(image)) / (numpy.max(image) - numpy.min(image))
    for point in points:
        markedimage[point[1]][point[0]][0] = 1
        markedimage[point[1]][point[0]][1] = 0
        markedimage[point[1]][point[0]][2] = 0
        if point[0] > 0:
            markedimage[point[1]][point[0] - 1][0] = 1
            markedimage[point[1]][point[0] - 1][1] = 0
            markedimage[point[1]][point[0] - 1][2] = 0
        if point[1] > 0:
            markedimage[point[1] - 1][point[0]][0] = 1
            markedimage[point[1] - 1][point[0]][1] = 0
            markedimage[point[1] - 1][point[0]][2] = 0
        if point[0] < image.shape[1] - 1:
            markedimage[point[1]][point[0] + 1][0] = 1
            markedimage[point[1]][point[0] + 1][1] = 0
            markedimage[point[1]][point[0] + 1][2] = 0
        if point[1] < image.shape[0] - 1:
            markedimage[point[1] + 1][point[0]][0] = 1
            markedimage[point[1] + 1][point[0]][1] = 0
            markedimage[point[1] + 1][point[0]][2] = 0
    return markedimage

def testpointvsnoise(size = (21, 21), height = .75, noise = .25, breadth = 0):
    tstimg = numpy.ones(size)
    if breadth > 0:
        width = breadth**2 / (-1 * numpy.log(.1))
        radius = breadth
    else:
        width = ((numpy.min(size) - 1) / 4)**2 / (-1 * numpy.log(.1))
        radius = int((numpy.min(size) - 1) / 4)
    midpnt = [int((size[0] - 1) / 2), int((size[1] - 1) / 2)]
    for j in range(tstimg.shape[0]):
        for i in range(tstimg.shape[1]):
            tstimg[j][i] = height * numpy.exp(-1 * ((j - midpnt[0])**2 + (i - midpnt[1])**2) / width) + noise * numpy.random.rand()
    compix = numpy.zeros((3, 3, 2))
    for l in range(midpnt[0] - radius, midpnt[0] + radius + 1):
        if l == midpnt[0]:
            highx = radius
        else:
            highx = int(numpy.round((radius**2 - (numpy.abs(midpnt[0] - l) - .5)**2)**.5))
        for k in range(int(midpnt[1] - highx), int(midpnt[1] + highx + 1)):
            #viwwin[comprd - (j - l)][comprd - (i - k)] = orgimg[l][k]
            mnrdst = ((midpnt[1] - k)**2 + (midpnt[0] - l)**2)**.5
            if mnrdst <= radius / 2:
                compix[1][1][0] = compix[1][1][0] + tstimg[l][k]
                compix[1][1][1] = compix[1][1][1] + 1
            if mnrdst >= radius / 2:
                pntsin = (l - midpnt[0]) / mnrdst
                pntcos = (k - midpnt[1]) / mnrdst
                if pntcos == 1: # Border of sectors (1, 0) and (2, 0)
                    compix[0][2][0] = compix[0][2][0] + tstimg[l][k]
                    compix[1][2][0] = compix[1][2][0] + tstimg[l][k]
                    compix[2][2][0] = compix[2][2][0] + tstimg[l][k]
                    compix[0][2][1] = compix[0][2][1] + 1
                    compix[1][2][1] = compix[1][2][1] + 1
                    compix[2][2][1] = compix[2][2][1] + 1
                elif pntcos > 1 / 2**.5:
                    if pntsin > 0: # Sector (1, 0)
                        compix[1][2][0] = compix[1][2][0] + tstimg[l][k]
                        compix[2][2][0] = compix[2][2][0] + tstimg[l][k]
                        compix[1][2][1] = compix[1][2][1] + 1
                        compix[2][2][1] = compix[2][2][1] + 1
                    else: # Sector (2, 0)
                        compix[1][2][0] = compix[1][2][0] + tstimg[l][k]
                        compix[0][2][0] = compix[0][2][0] + tstimg[l][k]
                        compix[1][2][1] = compix[1][2][1] + 1
                        compix[0][2][1] = compix[0][2][1] + 1
                elif pntcos == 1 / 2**.5:
                    if pntsin > 0: # Border of sectors (0, 1) and (1, 0)
                        compix[1][2][0] = compix[1][2][0] + tstimg[l][k]
                        compix[2][2][0] = compix[2][2][0] + tstimg[l][k]
                        compix[2][1][0] = compix[2][1][0] + tstimg[l][k]
                        compix[1][2][1] = compix[1][2][1] + 1
                        compix[2][2][1] = compix[2][2][1] + 1
                        compix[2][1][1] = compix[2][1][1] + 1
                    else: # Border of sectors (3, 1) and (2, 0)
                        compix[1][2][0] = compix[1][2][0] + tstimg[l][k]
                        compix[0][2][0] = compix[0][2][0] + tstimg[l][k]
                        compix[0][1][0] = compix[0][1][0] + tstimg[l][k]
                        compix[1][2][1] = compix[1][2][1] + 1
                        compix[0][2][1] = compix[0][2][1] + 1
                        compix[0][1][1] = compix[0][1][1] + 1
                elif pntcos > 0:
                    if pntsin > 0: # Sector (0, 1)
                        compix[2][2][0] = compix[2][2][0] + tstimg[l][k]
                        compix[2][1][0] = compix[2][1][0] + tstimg[l][k]
                        compix[2][2][1] = compix[2][2][1] + 1
                        compix[2][1][1] = compix[2][1][1] + 1
                    else: # Sector (3, 1)
                        compix[0][2][0] = compix[0][2][0] + tstimg[l][k]
                        compix[0][1][0] = compix[0][1][0] + tstimg[l][k]
                        compix[0][2][1] = compix[0][2][1] + 1
                        compix[0][1][1] = compix[0][1][1] + 1
                elif pntcos == 0:
                    if pntsin > 0: # Border of sectors (0, 1) and (0, 2)
                        compix[2][2][0] = compix[2][2][0] + tstimg[l][k]
                        compix[2][1][0] = compix[2][1][0] + tstimg[l][k]
                        compix[2][0][0] = compix[2][0][0] + tstimg[l][k]
                        compix[2][2][1] = compix[2][2][1] + 1
                        compix[2][1][1] = compix[2][1][1] + 1
                        compix[2][0][1] = compix[2][0][1] + 1
                    else: # Border of sectors (3, 1) and (3, 2)
                        compix[0][2][0] = compix[0][2][0] + tstimg[l][k]
                        compix[0][1][0] = compix[0][1][0] + tstimg[l][k]
                        compix[0][0][0] = compix[0][0][0] + tstimg[l][k]
                        compix[0][2][1] = compix[0][2][1] + 1
                        compix[0][1][1] = compix[0][1][1] + 1
                        compix[0][0][1] = compix[0][0][1] + 1
                elif pntcos > -1 / 2**.5:
                    if pntsin > 0: # Sector (0, 2)
                        compix[2][1][0] = compix[2][1][0] + tstimg[l][k]
                        compix[2][0][0] = compix[2][0][0] + tstimg[l][k]
                        compix[2][1][1] = compix[2][1][1] + 1
                        compix[2][0][1] = compix[2][0][1] + 1
                    else: # Sector (3, 2)
                        compix[0][1][0] = compix[0][1][0] + tstimg[l][k]
                        compix[0][0][0] = compix[0][0][0] + tstimg[l][k]
                        compix[0][1][1] = compix[0][1][1] + 1
                        compix[0][0][1] = compix[0][0][1] + 1
                elif pntcos == -1 / 2**.5:
                    if pntsin > 0: # Border of sectors (0, 2) and (1, 3)
                        compix[2][1][0] = compix[2][1][0] + tstimg[l][k]
                        compix[2][0][0] = compix[2][0][0] + tstimg[l][k]
                        compix[1][0][0] = compix[1][0][0] + tstimg[l][k]
                        compix[2][1][1] = compix[2][1][1] + 1
                        compix[2][0][1] = compix[2][0][1] + 1
                        compix[1][0][1] = compix[1][0][1] + 1
                    else: # Border of sectors (3, 2) and (2, 3)
                        compix[0][1][0] = compix[0][1][0] + tstimg[l][k]
                        compix[0][0][0] = compix[0][0][0] + tstimg[l][k]
                        compix[1][0][0] = compix[1][0][0] + tstimg[l][k]
                        compix[0][1][1] = compix[0][1][1] + 1
                        compix[0][0][1] = compix[0][0][1] + 1
                        compix[1][0][1] = compix[1][0][1] + 1
                elif pntcos > -1:
                    if pntsin > 0: # Sector (1, 3)
                        compix[2][0][0] = compix[2][0][0] + tstimg[l][k]
                        compix[1][0][0] = compix[1][0][0] + tstimg[l][k]
                        compix[2][0][1] = compix[2][0][1] + 1
                        compix[1][0][1] = compix[1][0][1] + 1
                    else: # Sector (2, 3)
                        compix[0][0][0] = compix[0][0][0] + tstimg[l][k]
                        compix[1][0][0] = compix[1][0][0] + tstimg[l][k]
                        compix[0][0][1] = compix[0][0][1] + 1
                        compix[1][0][1] = compix[1][0][1] + 1
                elif pntcos == -1: # Border of sectors (1, 3) and (2, 3)
                    compix[2][0][0] = compix[2][0][0] + tstimg[l][k]
                    compix[1][0][0] = compix[1][0][0] + tstimg[l][k]
                    compix[0][0][0] = compix[0][0][0] + tstimg[l][k]
                    compix[2][0][1] = compix[2][0][1] + 1
                    compix[1][0][1] = compix[1][0][1] + 1
                    compix[0][0][1] = compix[0][0][1] + 1
    minhgt = compix[1][1][0]
    for n in range(compix.shape[0]):
        for m in range(compix.shape[1]):
            if compix[n][m][1] > 0:
                compix[n][m][0] = compix[n][m][0] / compix[n][m][1]
                if compix[n][m][0] < minhgt:
                    minhgt = compix[n][m][0]
    if minhgt == compix[1][1][0]:
        nrmpix = compix[:, :, 0] / minhgt
    else:
        nrmpix = (compix[:, :, 0] - minhgt) / (compix[1][1][0] - minhgt)
    print(f'Height, noise, width, radius, value 1, value 2, value 3, value 4, value 5, value 6, value 7, value 8')
    print([height, noise, width, radius, nrmpix[0][0], nrmpix[0][1], nrmpix[0][2], nrmpix[1][0], nrmpix[1][2], nrmpix[2][0], nrmpix[2][1], nrmpix[2][2]])
    fig, ax = mpl.subplots(1, 2)
    ax[0].imshow(tstimg)
    ax[1].imshow(nrmpix)

if __name__ == '__main__':
# =============================================================================
#     testpointvsnoise(height = .15 * numpy.random.rand() + .1)
#     testpointvsnoise(height = .15 * numpy.random.rand() + .1)
#     testpointvsnoise(height = .15 * numpy.random.rand() + .1)
#     testpointvsnoise(height = .15 * numpy.random.rand() + .1)
#     testpointvsnoise(height = .15 * numpy.random.rand() + .1)
# =============================================================================
    flname = input('Please enter the name of your file: ')
    [fname, ftype] = flname.split('.')
    orgimg = numpy.genfromtxt(flname, delimiter = ',')
    comprd = 3
    iddimg = imageevaluation(orgimg, comprd)
    atomlocations = pointdetection(iddimg, comprd)
    locatedimage = markpositions(orgimg, atomlocations)
    mpl.figure()
    mpl.imshow(orgimg)
    mpl.figure()
    mpl.imshow(visualizecategoryimage(iddimg))
    mpl.figure()
    mpl.imshow(locatedimage)
# =============================================================================
#     fig, ax = mpl.subplots(1, 3)
#     ax[0].imshow(viwwin)
#     ax[1].imshow(compix[:, :, 0])
#     if categ[0] == 0:
#         ax[2].imshow(catega)
#     elif categ[0] == 1:
#         ax[2].imshow(categb[categ[1]])
#     elif categ[0] == 2:
#         ax[2].imshow(categc[categ[1]])
#     elif categ[0] == 3:
#         ax[2].imshow(categd[categ[1]])
#     else:
#         ax[2].imshow(catege)
# =============================================================================
