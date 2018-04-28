# gst-filter
Simple Python Gstreamer Overlay Plugin.
Overlay implemented with OpenCV, PyCairo

### How to run

    git clone https://github.com/jackersson/gst-overlay.git
    cd gst-overlay

    python3 run.py -f car.mpg -i cat/ --cairo
    python3 run.py -f car.mpg -i cat/ --opencv
    python3 run.py -f car.mpg -i cat/ --cairo --fps