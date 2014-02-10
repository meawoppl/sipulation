from pylab import *

from scipy import *
from scipy import misc, interpolate, spatial, random, ndimage


def nRandomImagePoint(image, n):
    # Compute a CDF function across the flattened image
    imageCDF = image.flatten().cumsum()
    imageCDF /= 1.0 * imageCDF.max()

    # Function to turn a random point in the CDF into a random index in the image
    indexInterpolator = interpolate.interp1d(imageCDF, arange(imageCDF.size))

    # Set to collect the UNIQUE indices
    indexContainer = set()
    while len(indexContainer) < n:
        # Generate at most the number of points remaining
        maxToGenerate = n - len(indexContainer)
        randomCDFValues = random.uniform(0, 1.0, maxToGenerate)

        # Back them into indices
        iInterp = indexInterpolator(randomCDFValues)
        iInterp = np.round(iInterp).astype(uint32)

        # Add them to the set
        indexContainer.update(iInterp)

    # Break them out of the set
    iInterp = array(list(indexContainer))

    # Compute the equivalent xy
    xCoords = (iInterp // image.shape[0]).astype(int32)
    yCoords = (iInterp %  image.shape[0]).astype(int32)

    # Return them glued together.
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
