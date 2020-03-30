# http://setosa.io/ev/image-kernels/
# https://docs.gimp.org/2.8/en/plug-in-convmatrix.html

import numpy as np
from PyVutils import Cv

im = Cv.Load("data/57338813_2279331262305612_7257596330455859200_n.jpg")
im = Cv.ScaleImage(im, 500)

identity = np.array(
[
	[+0.0, +0.0, +0.0],
	[+0.0, +1.0, +0.0],
	[+0.0, +0.0, +0.0],
])

sharpen = np.array(
[
	[+0.0, -1.0, +0.0],
	[-1.0, +5.0, -1.0],
	[+0.0, -1.0, +0.0],
])

blur = np.array(
[
	[+0.1, +0.1, +0.1],
	[+0.1, +0.1, +0.1],
	[+0.1, +0.1, +0.1],
])

images = []

im_filtered = Cv.Conv2D(im, identity)
images.append(im)

im_filtered = Cv.Conv2D(im, blur)
images.append(im_filtered)

im_filtered = Cv.Conv2D(im, sharpen)
images.append(im_filtered)

Cv.Display(Cv.Collage(images, Cv.CV_HSTACK))