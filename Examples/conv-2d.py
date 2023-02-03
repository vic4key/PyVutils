# http://setosa.io/ev/image-kernels/
# https://docs.gimp.org/2.8/en/plug-in-convmatrix.html

import numpy as np
import PyVutils as vu

image = vu.load_image("data/test.jpg")
image = vu.scale_image(image, 500)

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

im_filtered = vu.conv_2d(image, identity)
images.append(image)

im_filtered = vu.conv_2d(image, blur)
images.append(im_filtered)

im_filtered = vu.conv_2d(image, sharpen)
images.append(im_filtered)

result = vu.display_collage_images(images, vu.CV_HSTACK)
vu.save_image("data/test_filtered.jpg", result)

vu.display_image(result)

'''
<data/test_filtered.jpg>
'''