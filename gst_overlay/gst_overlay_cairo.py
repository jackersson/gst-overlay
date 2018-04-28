import os
import cairo
import logging
import numpy as np
import cv2
import glob
import timeit
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
from gi.repository import Gst, GObject, GstBase

from .gst_hacks import map_gst_buffer, get_buffer_size

GST_OVERLAY_CAIRO = 'gstoverlaycairo'


# https://lazka.github.io/pgi-docs/GstBase-1.0/classes/BaseTransform.html
class GstOverlayCairo(GstBase.BaseTransform):

    CHANNELS = 4  # RGBx

    __gstmetadata__ = ("An example plugin of GstOverlayCairo",
                       "gst-filter/gst_overlay_cairo.py",
                       "gst.Element draw on image",
                       "Taras at LifeStyleTransfer.com")

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string("video/x-raw,format=RGBx")),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string("video/x-raw,format=RGBx")))
    
    def __init__(self):
        super(GstOverlayCairo, self).__init__()  

        # Overlay could be any of your objects as far as it implements __call__
        # and returns cairo.Surface
        self.overlay = None

    def do_transform_ip(self, inbuffer):
        """
            Implementation of simple filter.
            All changes affected on Inbuffer

            Read more:
            https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-libs/html/GstBaseTransform.html
        """

        success, (width, height) = get_buffer_size(self.srcpad.get_current_caps())
        if not success:
            # https://lazka.github.io/pgi-docs/Gst-1.0/enums.html#Gst.FlowReturn
            return Gst.FlowReturn.ERROR
       
        with map_gst_buffer(inbuffer, Gst.MapFlags.READ) as mapped:
            self._draw(mapped, width, height)

        return Gst.FlowReturn.OK


    def _draw(self, buffer, width, height):
        try:     
            # https://pycairo.readthedocs.io/en/latest/reference/surfaces.html#cairo.ImageSurface.format_stride_for_width
            stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_RGB24, width)

            # https://pycairo.readthedocs.io/en/latest/reference/surfaces.html#cairo.ImageSurface.create_for_data
            surface = cairo.ImageSurface.create_for_data(buffer, cairo.FORMAT_RGB24, 
                                                         width, height, stride)
            # Documentation: https://pycairo.readthedocs.io/en/latest/reference/context.html
            context = cairo.Context(surface)

            # draw image
            overlay = self.overlay()
            x = width - overlay.get_width()
            y = height - overlay.get_height()

            # Documentation: https://www.cairographics.org/FAQ/
            # How do I paint on surface
            context.set_source_surface(self.overlay(), x, y)
            context.paint()
        except Exception as e:
            logging.error(e)
            logging.error("Failed to create cairo surface for buffer")


def register(plugin):
    # https://lazka.github.io/pgi-docs/#GObject-2.0/functions.html#GObject.type_register
    type_to_register = GObject.type_register(GstOverlayCairo)

    # https://lazka.github.io/pgi-docs/#Gst-1.0/classes/Element.html#Gst.Element.register
    return Gst.Element.register(plugin, GST_OVERLAY_CAIRO, 0, type_to_register)       


def register_by_name(plugin_name):
    
    # Parameters explanation
    # https://lazka.github.io/pgi-docs/Gst-1.0/classes/Plugin.html#Gst.Plugin.register_static
    name = plugin_name
    description = "gst.Element draws on image buffer"
    version = '1.12.4'
    gst_license = 'LGPL'
    source_module = 'gstreamer'
    package = 'gstoverlay'
    origin = 'lifestyletransfer.com'
    if not Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR,
                                      name, description,
                                      register, version, gst_license,
                                      source_module, package, origin):
        raise ImportError("Plugin {} not registered".format(plugin_name)) 
    return True

register_by_name(GST_OVERLAY_CAIRO)

