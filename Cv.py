# -*- coding: utf-8 -*-

# Vutils for OpenCV

import sys, cv2, imutils
import numpy as np
import random as rd

# ---

IT_COLOR = cv2.IMREAD_COLOR
IT_GRAY  = cv2.IMREAD_GRAYSCALE
IT_UNCHANGED = cv2.IMREAD_UNCHANGED

def LoadImage(filePath, type = IT_COLOR) :
    return cv2.imread(filePath, IT_COLOR)

def SaveImage(filePath, image) :
    cv2.imwrite(filePath, image)
    return

def DisplayImage(image, windowTitle = "Sample", forceExit = False) :
    cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(windowTitle, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if forceExit : sys.exit(0)
    return

def DisplayCapture(sourceType, fnCallback, windowTitle, *args) :
    vkSpace     = 0x20 # Space
    vkEscape    = 0x1B # Esc
    vkReturn    = 0x0D # Enter

    # https://docs.opencv.org/3.1.0/dd/de7/group__videoio.html
    # http://eitguide.net/su-dung-videocapture-trong-opencv/

    camera = cv2.VideoCapture(sourceType)

    while camera.isOpened():
        ok, frame = camera.read()
        if not ok : break
        frame = cv2.flip(frame, 1)
        frame = fnCallback(frame, args)
        if type(frame).__name__ != "ndarray":
            camera.release()
            raise TypeError("Missing returned frame from the callback function")
        cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(windowTitle, frame)
        if (cv2.waitKey(1) & 0xFF) in [vkSpace, vkEscape, vkReturn] : break
    pass

    cv2.destroyAllWindows()
    camera.release()

    return

def DisplayCamera(fnCallback, windowTitle = "Sample", *args):

    if type(fnCallback).__name__ != "function" or fnCallback.__code__.co_argcount != 1 :
        msg  = "fnCallback` argument must be a callback function"
        msg += " "
        msg += "`Eg. Callback(frame, *args) -> frame"
        raise NameError(msg)

    ocvDisplayCapture(cv2.CAP_ANY, fnCallback, windowTitle, args)

    return

def DisplayVideo(videoFilePath, fnCallback, windowTitle = "Sample", *args):

    if type(fnCallback).__name__ != "function" or fnCallback.__code__.co_argcount != 1 :
        msg  = "fnCallback` argument must be a callback function"
        msg += " "
        msg += "`Eg. Callback(frame, *args) -> frame"
        raise NameError(msg)

    ocvDisplayCapture(videoFilePath, fnCallback, windowTitle, args)

    return

DEFAULT_COLOR = (0, 255, 0)

def DrawText(image, x, y, text, scale = 1.0, color = DEFAULT_COLOR, thickness = 1) :
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 1, cv2.LINE_8)
    return

def DrawRectangle(image, x, y, width, height, color = DEFAULT_COLOR, thickness = 1) :
    cv2.rectangle(image, (x, y), (x + width, y + height), color, thickness, cv2.LINE_8)
    return

# shape : image.shape or [width, height, nChannel]
# color : 255 -> white or 0 -> black
def CreateBlankImage(shape, color = 255) :
    image = np.zeros(shape, np.uint8)
    image[:,:,] = color
    return image

# shape = [width, height, 3]
def CreateBlankBgrImage(shape, color = (255, 255, 255)) :
    image = np.zeros(shape, np.uint8)
    image[:,:,] = color
    return image

def ToGray(bgrImage) :
    return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)

def ToHSV(bgrImage) :
    return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2HSV)

# https://docs.opencv.org/3.4.0/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d
def ScaleImageByRatio(image, scale, itplMethod = cv2.INTER_CUBIC) :
    return cv2.resize(image, None, fx = scale, fy = scale, interpolation = itplMethod)

# aspectRatio = True : The image will be scaled following `width` or `height` if only pass one of them.
# It means `width` or `height` is auto calculating by one of them.
def ScaleImage(image, width = None, height = None, aspectRatio = True, itplMethod = cv2.INTER_CUBIC) :

    if width is None and height is None : return image

    w, h, n = image.shape

    defaultScale = 1.0

    scaleX = float(1.0 / (w / width))  if width is not None else defaultScale
    scaleY = float(1.0 / (h / height)) if height is not None else defaultScale

    if aspectRatio :
        if height is None and width is not None :
            scaleY = scaleX
        elif width is None and height is not None :
            scaleX = scaleY
    pass

    return cv2.resize(image, None, fx = scaleX, fy = scaleY, interpolation = itplMethod)

def CreateImageMaskByColorFromHsvImage(hsvImage, color, delta = 10) :

    b, g, r = color

    mask_rgb_color = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)

    mask_hsv_color_lower = np.array([mask_rgb_color[0][0][0] - delta, 100, 100])
    mask_hsv_color_upper = np.array([mask_rgb_color[0][0][0] + delta, 255, 255])

    mask = cv2.inRange(hsvImage, mask_hsv_color_lower, mask_hsv_color_upper)

    return mask


def CreateImageMaskByColor(bgrImage, color, delta = 10, invertMask = True) :
    hsv = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2HSV)

    mask = ocvCreateImageMaskByColorFromHsvImage(hsv, color, delta)
    if invertMask : mask = cv2.bitwise_not(mask)

    return mask

def CreateImageMaskByColors(bgrImage, colors, delta = 10, invertMask = True) :

    hsv = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2HSV)

    masks = None

    for color in colors :
        mask = ocvCreateImageMaskByColorFromHsvImage(hsv, color, delta)
        if masks is None : masks = mask
        else : masks = cv2.add(masks, mask)
    pass

    if invertMask : masks = cv2.bitwise_not(masks)

    return masks

CN_BLUE  = 0
CN_GREEN = 1
CN_RED   = 2

def CombineRGB(image, channel):
    cn_image = cv2.split(image)[channel]
    return cv2.merge((cn_image, cn_image, cn_image))

def RandomRGB(low = 0, high = 255):
    r = rd.randint(low, high)
    g = rd.randint(low, high)
    b = rd.randint(low, high)
    return (r, g, b)

# https://docs.opencv.org/3.4.0/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71
# method: cv.RETR_EXTERNAL, cv.RETR_LIST, cv.RETR_CCOMP, cv.RETR_TREE, cv.RETR_FLOODFILL
def FindContours(imageGray, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE) :
    contours = cv2.findContours(imageGray.copy(), mode, method)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    return contours

# thickness: 0, cv2.FILLED
def DrawContour(image, contour, color = (0, 255, 0), thickness = 1):
    cv2.drawContours(image, [contour], -1, color, thickness)
    return
