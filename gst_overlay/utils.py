import cairo
import cv2

import os

import datetime
import glob


def list_files(folder, file_format='.jpg'):   
    """
        List files in folder with specific pattern

        :param folder:
        :type folder: str

        :param file_format: .{your format}
        :type file_format: str

        :rtype: list[str] (Absolute paths to files)
    """ 
    pattern = '{0}/*{1}'.format(folder, file_format)
    filenames = glob.glob(pattern)    
    return filenames


def draw_image(source, image, x, y):
    """
        Places "image" with alpha channel on "source" at x, y

        :param source:  
        :type source: numpy.ndarray

        :param image:  
        :type image: numpy.ndarray (with alpha channel)

        :param x: 
        :type x: int

        :param y:  
        :type y: int

        :rtype: numpy.ndarray
    """
    h, w = image.shape[:2]    
    
    max_x, max_y = x + w, y + h      
    alpha = image[:, :, 3] / 255.0
    for c in range(0, 3):
        color = image[:, :, c] * (alpha)
        beta = source[y:max_y, x:max_x, c] * (1.0 - alpha)
        source[y:max_y, x:max_x, c] = color + beta
    return source


def load_image_cv(filename):
    """
        :param filename:  
        :type filename: str

        :rtype: numpy.ndarray
    """
    assert os.path.isfile(filename), "Invalid filename: {}".format(filename)
    return cv2.imread(filename, -1)


def load_image_cairo(filename):
    """
        :param filename:  
        :type filename: str

        :rtype: cairo.Surface
    """
    assert os.path.isfile(filename), "Invalid filename: {}".format(filename)
    return cairo.ImageSurface.create_from_png(filename)
