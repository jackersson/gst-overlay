# gst-filter
Simple Python Gstreamer Overlay Plugin.
Overlay implemented with OpenCV, PyCairo

### How to run

    git clone https://github.com/jackersson/gst-overlay.git
    cd gst-overlay

    python3 run.py -f car.mpg -i cat/ --cairo
    python3 run.py -f car.mpg -i cat/ --opencv
    python3 run.py -f car.mpg -i cat/ --cairo --fps
    
    
### Flags
- -f, --file - video file's absolute path
- -i, --images - existing folder with images to be draw on video
- --cairo - use Cairo drawing call
- --opencv - use OpenCV drawing call
- --fps - draw FPS on video
 
Test car (video) and kitten (.png animation) from blog post download from [here](https://drive.google.com/drive/folders/1Vd0sRuW9BE2md6idEq6wYWYb6jWRkaju?usp=sharing)
