import os
from .utils import list_files, load_image_cairo, load_image_cv


class Animation(object):

    def __init__(self, images, keyframe=5):
        """

            :param images: contains images
            :type images: list

            :param images: makes animation slower[0]/faster[maxint]
            :type images: keyframe [0, maxint]
        """
        assert len(images), "Invalid data. Empty Images: {}".format(len(images))
        self._images = images
        self._image_id, self._frame_id = 0, 0

        self._keyframe = keyframe
    
    def __call__(self):
        """
            Returns next image when call:
                a = Animation(items)
                image = a()

            :rtype: image_type (numpy, cairo.surface, etc.)
        """

        # Keyframe makes animation faster/slower
        self._frame_id += 1
        if self._frame_id >= self._keyframe:
            self._frame_id = 0
            self._image_id += 1

        if self._image_id >= len(self._images):
            self._image_id = 0

        return self._images[self._image_id]


def create_animation_from_folder_cairo(folder, file_format=".png"):
    assert os.path.isdir(folder), "Invalid folder: {}".format(folder)
    return Animation([load_image_cairo(fl) for fl in list_files(folder, file_format=file_format)])


def create_animation_from_folder_cv(folder, file_format=".png"):
    assert os.path.isdir(folder), "Invalid folder: {}".format(folder)
    return Animation([load_image_cv(fl) for fl in list_files(folder, file_format=file_format)])