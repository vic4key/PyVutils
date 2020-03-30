# http://setosa.io/ev/image-kernels/
# https://docs.gimp.org/2.8/en/plug-in-convmatrix.html

import numpy as np
from PyVutils import Cv

im = Cv.Load("data/test.jpg")
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

result = Cv.Collage(images, Cv.CV_HSTACK)
Cv.Save("data/test_filtered.jpg", result)

Cv.Display(result)

'''
<data/test_filtered.jpg>
'''