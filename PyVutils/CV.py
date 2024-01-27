# -*- coding: utf-8 -*-

# Vutils for OpenCV

import sys, cv2, imutils
import numpy as np
import random as rd
from typing import Union
from multipledispatch import dispatch

from .Math import *

# ---

point_2d = Union[Point2D, tuple]

CV_COLOR = cv2.IMREAD_COLOR
CV_GRAY  = cv2.IMREAD_GRAYSCALE
CV_UNCHANGED = cv2.IMREAD_UNCHANGED

def load_image(file_path, type = CV_COLOR):
    return cv2.imread(file_path, CV_COLOR)

def save_image(file_path, image):
    cv2.imwrite(file_path, image)
    return

def display_image(image, window_title = "Image", forceExit = False):
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(window_title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if forceExit : sys.exit(0)
    return

def _video_capture(source, fn, window_title, *args):
    vkSpace     = 0x20 # Space
    vkEscape    = 0x1B # Esc
    vkReturn    = 0x0D # Enter

    # https://docs.opencv.org/3.1.0/dd/de7/group__videoio.html
    # http://eitguide.net/su-dung-videocapture-trong-opencv/

    cap = cv2.VideoCapture(source)

    iframe = 0
    nframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok : break

        if nframe == -1: # flip if camera
            frame = cv2.flip(frame, 1)

        iframe += 1
        frame = fn(frame, (iframe, nframe), args)

        if type(frame).__name__ != "ndarray":
            cap.release()
            raise TypeError("Missing returned frame from the callback function")

        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_title, frame)

        if (cv2.waitKey(10) & 0xFF) in [vkEscape] : break
    pass

    cv2.destroyAllWindows()
    cap.release()

    return

def webcam(fn, window_title = "Webcam", *args):

    if type(fn).__name__ != "function" or fn.__code__.co_argcount != 2 :
        msg  = "fn` argument must be a callback function"
        msg += " "
        msg += "`Eg. callback(frame, frameinfo, *args) -> frame"
        raise NameError(msg)

    _video_capture(cv2.CAP_ANY, fn, window_title, args)

    return

def play_video(video_file_path, fn, window_title = "Video", *args):

    if type(fn).__name__ != "function" or fn.__code__.co_argcount != 2 :
        msg  = "fn` argument must be a callback function"
        msg += " "
        msg += "`Eg. callback(frame, frameinfo, *args) -> frame"
        raise NameError(msg)

    _video_capture(video_file_path, fn, window_title, args)

    return

COLOR_BLACK   = (0x00, 0x00, 0x00)
COLOR_WHITE   = (0xFF, 0xFF, 0xFF)
COLOR_RED     = (0x00, 0x00, 0xFF)
COLOR_GREEN   = (0x00, 0xFF, 0x00)
COLOR_BLUE    = (0xFF, 0x00, 0x00)
COLOR_PINK    = (0xFF, 0x00, 0xFF)
COLOR_CYAN    = (0xFF, 0xFF, 0x00)
COLOR_YELLOW  = (0x00, 0xFF, 0xFF)

DEFAULT_COLOR = COLOR_GREEN

def draw_text(image, x, y, text, scale = 1.0, color = DEFAULT_COLOR, thickness = 1):
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 1, cv2.LINE_8)

def draw_line(image, p1: point_2d, p2: point_2d, color: tuple = DEFAULT_COLOR, thickness: int = 1):
    if type(p1) is Point2D: p1 = p1.to_tuple(ValueType.Integer)
    if type(p2) is Point2D: p2 = p2.to_tuple(ValueType.Integer)
    cv2.line(image, p1, p2, color, thickness)

# @dispatch(np.ndarray, int, int, int, int, tuple, int)
# def draw_line(image, x1, y1, x2, y2, color: tuple = DEFAULT_COLOR, thickness: int = 1):
#     cv2.line(image, (x1, y1), (x2, y2), color, thickness)

def draw_rectangle(image, x, y, width, height, color = DEFAULT_COLOR, thickness = 1):
    cv2.rectangle(image, (x, y), (x + width, y + height), color, thickness, cv2.LINE_8)

def draw_marker(image, point: point_2d, size: int = 5, color: tuple = DEFAULT_COLOR, thickness: int = 1):
    if type(point) is tuple: x, y = point
    elif type(point) is Point2D: x, y = point.x, point.y
    p1 = Point2D(x - size, y - size)
    p2 = Point2D(x + size, y + size)
    p3 = Point2D(x + size, y - size)
    p4 = Point2D(x - size, y + size)
    draw_line(image, p1, p2, color, thickness)
    draw_line(image, p3, p4, color, thickness)
    # draw_line(image, x + size, y - size, x + size, y + size, color, thickness)

# shape = [width, height, channel] eg. [480, 280, 3]
def create_blank_image(shape, color = COLOR_WHITE):
    image = np.zeros(shape, np.uint8)
    image[:,:,] = color
    return image

def to_gray_image(bgr_image):
    return cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

def to_hsv_image(bgr_image):
    return cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

def normalize_image(image):
    return image / 255.0

def conv_2d(image, kernel):
    return cv2.filter2D(image, -1, kernel)

# https://docs.opencv.org/3.4.0/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d
def scale_mage_by_ratio(image, scale, method = cv2.INTER_CUBIC):
    return cv2.resize(image, None, fx = scale, fy = scale, interpolation = method)

# aspect_ratio = True : The image will be scaled following `width` or `height` if only pass one of them.
# It means `width` or `height` is auto calculating by one of them.
def scale_image(image, width = None, height = None, aspect_ratio = True, method = cv2.INTER_CUBIC):

    if width is None and height is None : return image

    w, h, n = image.shape

    defaultScale = 1.0

    scaleX = float(1.0 / (w / width))  if width is not None else defaultScale
    scaleY = float(1.0 / (h / height)) if height is not None else defaultScale

    if aspect_ratio :
        if height is None and width is not None :
            scaleY = scaleX
        elif width is None and height is not None :
            scaleX = scaleY
    pass

    return cv2.resize(image, None, fx = scaleX, fy = scaleY, interpolation = method)

def create_image_mask_by_color_from_hsv_image(hsv_image, color, delta = 10):

    b, g, r = color

    mask_rgb_color = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)

    mask_hsv_color_lower = np.array([mask_rgb_color[0][0][0] - delta, 100, 100])
    mask_hsv_color_upper = np.array([mask_rgb_color[0][0][0] + delta, 255, 255])

    mask = cv2.inRange(hsv_image, mask_hsv_color_lower, mask_hsv_color_upper)

    return mask


def create_image_mask_by_color(bgr_image, color, delta = 10, invert_mask = True):
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    mask = create_image_mask_by_color_from_hsv_image(hsv, color, delta)
    if invert_mask : mask = cv2.bitwise_not(mask)

    return mask

def create_image_mask_by_colors(bgr_image, colors, delta = 10, invert_mask = True):

    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    masks = None

    for color in colors :
        mask = create_image_mask_by_color_from_hsv_image(hsv, color, delta)
        if masks is None : masks = mask
        else : masks = cv2.add(masks, mask)
    pass

    if invert_mask : masks = cv2.bitwise_not(masks)

    return masks

CV_BLUE  = 0
CV_GREEN = 1
CV_RED   = 2

def split_rgb_channel(image, channel):
    cn_image = cv2.split(image)[channel]
    return cv2.merge((cn_image, cn_image, cn_image))

def random_rgb_pixel(low = 0, high = 255):
    r = rd.randint(low, high)
    g = rd.randint(low, high)
    b = rd.randint(low, high)
    return (r, g, b)

# https://docs.opencv.org/3.4.0/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71
# method: cv.RETR_EXTERNAL, cv.RETR_LIST, cv.RETR_CCOMP, cv.RETR_TREE, cv.RETR_FLOODFILL
def find_contours(image_gray, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE):
    contours = cv2.findContours(image_gray.copy(), mode, method)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    return contours

# thickness: 0, cv2.FILLED
def draw_contour(image, contour, color = (0, 255, 0), thickness = 1):
    cv2.drawContours(image, [contour], -1, color, thickness)

def extract_features(rgb_image, vector_size=32):
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()

        # Dinding image keypoints
        kps = alg.detect(rgb_image)

        # Getting first 32 of them.
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]

        # computing descriptors vector
        kps, result = alg.compute(rgb_image, kps)

        # Flatten all of them in one big vector - our feature vector
        result = result.flatten()

        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if result.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            result = np.concatenate([result, np.zeros(needed_size - result.size)])
    except cv2.error as e:
        print("Error: ", e)
        return None

    return result

def invert(image):
    return cv2.bitwise_not(image)

CV_VSTACK = 0
CV_HSTACK = 1

def display_collage_images(images, axis = CV_HSTACK):

    nimages = len(images)
    if nimages == 0: return None

    result = images[0]
    if nimages == 1: return result

    for image in images[1:]: result = np.concatenate((result, image), axis=axis)

    return result