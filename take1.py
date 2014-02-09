from pylab import *
from scipy import *
from scipy import misc, interpolate, spatial, random, ndimage

def nRandomImagePoint(image, n):
    imageCDF = 1.0 * image.cumsum(axis=0)
    colSum = image.sum(axis=0)
    
    # Avoid zero division rootnanny
    colSum[colSum == 0] = 1

    imageCDF /= colSum

    prob = (1.0 * colSum.cumsum()) / colSum.sum()

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

        pointContainer.append((x,y))

    print array(pointContainer).shape
    return array(pointContainer).T

def reLabel(image, noZero = True):
    unq, rIdx = unique(image, return_inverse=True)

    rng = arange(unq.size, dtype=uint64)
    if noZero:
        rIdx += 1
        rng += 1
    return rIdx.reshape(image.shape), rng

size = 1024
nPoints = 500

img = 255-misc.imread("StipplingOriginals/leaves_1024x1024_org.png", flatten=True)
shape = img.shape
xs, ys = nRandomImagePoint(img, nPoints)

points = c_[xs, ys]
spots = ones(shape, dtype=uint64)
for x in range(100):
    print("Starting")
    # Zero out the starting spot chart
    spots[:] = 1
    # Seed the voroni centers
    spots.flat[(xs +  ys*img.shape[0]).astype(uint64)] = 0

    # Compute the distances
    res = ndimage.distance_transform_edt(spots, return_distances=False, return_indices=True)
    print("EDT Done.")

    # Make unique group numbers out of the returned 
    cellNumber = res[0] + (res[1] * img.shape[0])
    cellNumber, unq = reLabel(cellNumber) # Make indices (1-nGroups)
    print cellNumber
    print("Relabel Done")  

    # imshow(cellNumber%23)
    # show()
    # 1/0    

    # Compute the centers of each group
    print img.shape, cellNumber.shape
    centers = ndimage.measurements.center_of_mass(img, labels=cellNumber, index=unq)
    print("Centers of Mass Done")

    print array(centers), len(centers)

    # Reassign the xs and ys, then start over
    xs, ys = array(centers).T


