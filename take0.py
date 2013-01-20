from pylab import *

from scipy import *
from scipy import misc, interpolate


def uniformPointFeild(shape, pointCount):
    xys = random.uniform(0.0, 1.0, (2, pointCount))
    xys *= array(shape).reshape((2,1))
    return xys


def imageAxisCDF(image, axis=0):
    if axis == 0:
        tempImage = image.copy()
    elif axis == 1:
        tempImage = image.T.copy()

    axisIntensity = tempImage.cumsum(axis=0)
    axisIntensity /= 1.0 * axisIntensity[-1,:]
    return axisIntensity

def realignX(pts, image):
    imagexCDF = imageAxisCDF(image)
    x, y = pts
    print x.min(), "-", x.max()
    print y.min(), "-", y.max()

    x_distance  = linspace(0.0, 1.0, image.shape[0])
    for yi in range(image.shape[1]):
        # figure()
        # plot(imagexCDF[:, 255])
        # show()
        # 1/0
        figure()
        print imagexCDF[:,yi]
        plot(imagexCDF[:,yi])
        show()
        currentCDFInterp = interpolate.interp1d(x_distance, imagexCDF[:,yi])
        currentXS = (y > yi) & (y < (yi+1))
        xCount = sum(1 * currentXS)
        x[currentXS] = currentCDFInterp(linspace(0.0, 1.0, xCount))

        print xCount
        print x[currentXS], y[currentXS]
        plot(x[currentXS], y[currentXS], "ro")
        show()
        1/0


    return c_[x,y]

img = 255-misc.imread("StipplingOriginals/figure5_525x525.png", flatten=True)
pts = uniformPointFeild(img.shape, 10000)

close("all")

# figure()
# imshow(img)
# axis("image")
# colorbar()

figure()
imshow(imageAxisCDF(img))
axis("image")
colorbar()
show()

pts = realignX(pts, img)

figure()
imshow(img)
plot(pts[:,1], pts[:,0] , 'bo')
show()

# pts = uniformPointFeild((10,20), 100)

# realignX(pts)


# print pts
# plot(pts[:,0], pts[:,1], 'bo', alpha=0.5)
# axis("image")
# show()
