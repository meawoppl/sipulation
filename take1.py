from pylab import *

from scipy import *
from scipy import misc, interpolate, spatial, random


def imageCDF(image):
    cdf = 1.0 * image.cumsum(axis=0)
    colSum = image.sum(axis=0)
    
    # Avoid zero division rootnanny
    colSum[colSum == 0] = 1

    cdf /= colSum

    colProb = (1.0 * colSum.cumsum()) / colSum.sum()

    return cdf, colProb

def nRandomImagePoint(imageCDF, prob, n):
    pointContainer = []

    xInterp = interpolate.interp1d(prob, linspace(0.0, 1.0, prob.shape[0]))

    while( len(pointContainer) < n):
        xN = random.uniform( 0.0, 1.0 )

        x = xInterp(xN) * imageCDF.shape[1]

        print xN, x

        # Values of the columns straddling point
        colBelow = imageCDF[:,floor(x)]
        colAbove = imageCDF[:, ceil(x)]
        
        delta = ceil(x) - x
        
        # Weighted average of the two CDF's 
        colCDF = (colBelow * delta) + (colAbove * (1.0-delta))

        if colCDF.sum() == 0:
            continue

        yInterp = interpolate.interp1d( colCDF, linspace(0.0, 1.0, colCDF.shape[0]))

        y = yInterp( random.uniform(0.0, 1.0)) * colCDF.shape[0]
        if (y == 0) or (y == colCDF.shape[0]):
            continue

        print x, y
        pointContainer.append((x,y))


    return array(pointContainer)


img = 255-misc.imread("StipplingOriginals/figure5_525x525.png", flatten=True)

iCDF, prob = imageCDF(img)

p = nRandomImagePoint(iCDF, prob, 1000)

imshow(img)
gray()

plot(p[:,0], p[:,1], "bo")

show()
