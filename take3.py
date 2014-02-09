from pylab import *

from scipy import *
from scipy import misc, interpolate, spatial, random, ndimage


def nRandomImagePoint(image, n):
    imageCDF = image.flatten().cumsum()
    imageCDF /= 1.0 * imageCDF[-1]

    pointContainer = []

    indexInterpolator = interpolate.interp1d(imageCDF, arange(imageCDF.size))
    randomCDFValues = random.uniform(0.0, 1.0, size=n)

    iInterp = indexInterpolator(randomCDFValues)

    print iInterp, image.size

    xCoords = (iInterp // image.shape[0]).astype(int32)
    yCoords = (iInterp %  image.shape[0]).astype(int32)

    print xCoords.ptp()
    print yCoords.ptp()

    # Now lets add +- 1 px in each direction so we dont get point stacking
    xCoords = xCoords + random.uniform(-1.0, 1.0, size=xCoords.size)
    yCoords = yCoords + random.uniform(-1.0, 1.0, size=yCoords.size)

    return c_[xCoords, yCoords]

size = 1024
nPoints = 5000

img = 255-misc.imread("StipplingOriginals/leaves_1024x1024_org.png", flatten=True)
img = 255-misc.imread("StipplingOriginals/figure5_700x700.png", flatten=True)

shape = img.shape
xys = nRandomImagePoint(img, nPoints)

figure()
# imshow(255 - img)
# gray()
plot(xys[:,1], -xys[:,0], "bo", )
show()
