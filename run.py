
import os
import logging
import traceback
import argparse 

# Required imports 
# Gst, GstBase, GObject
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Init Gobject Threads
# Init Gstreamer
GObject.threads_init()
Gst.init(None)

from gst_overlay.gstpipeline import GstPipeline
from gst_overlay.gst_overlay_opencv import GstOverlayOpenCv
from gst_overlay.gst_overlay_cairo import GstOverlayCairo
from gst_overlay.animation import create_animation_from_folder_cairo, create_animation_from_folder_cv
# Set logging level=DEBUG
logging.basicConfig(level=0)

# How to use argparse:
# https://www.pyimagesearch.com/2018/03/12/python-argparse-command-line-arguments/
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to video file")
ap.add_argument("-i", "--images", required=True, help="Path to folder with images")
ap.add_argument("-o", "--opencv", action='store_true', help="ON/OFF opencv overlay")
ap.add_argument("-c", "--cairo", action='store_true', help="ON/OFF cairo overlay")
ap.add_argument("--fps", action='store_true', help="ON/OFF show fps")
args = vars(ap.parse_args())


file_name = os.path.abspath(args['file'])
if not os.path.isfile(file_name):
    raise ValueError('File {} not exists'.format(file_name))

with_fps = args["fps"]

overlay, overlay_plugin_name = None, "overlay"

# Build pipeline
# filesrc https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-filesrc.html
# decodebin https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-decodebin.html
# videoconvert https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-videoconvert.html
# gtksink https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-good/html/gst-plugins-good-plugins-gtksink.html
# fpsdisplaysink https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad/html/gst-plugins-bad-plugins-fpsdisplaysink.html
command = 'filesrc location={} ! '.format(file_name)
command += 'decodebin ! '
command += 'videoconvert ! '

if args['opencv']:
    overlay = create_animation_from_folder_cv(args["images"])
    command += 'gstoverlayopencv name={} ! '.format(overlay_plugin_name)
else:
    overlay = create_animation_from_folder_cairo(args["images"])
    command += 'gstoverlaycairo name={} ! '.format(overlay_plugin_name)
    
command += 'videoconvert ! '
if args["fps"]:
    command += 'fpsdisplaysink video-sink=gtksink sync=false'
else:
    command += 'gtksink sync=false'

# Create pipeline
pipeline = GstPipeline(command)

# Set GstOverlay_.overlay to Animation from folder
# Overlay could be any of your objects as far as it implements __call__
ret, element = pipeline.get_element(overlay_plugin_name)
assert ret, "Can't get GstOverlay Element"
element.overlay = overlay

# Start pipeline
pipeline.start()

# Init GObject loop to handle Gstreamer Bus Events
loop = GObject.MainLoop()

try:
    loop.run()
except:
    traceback.print_exc()

pipeline.stop()