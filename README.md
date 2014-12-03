Human event detection
=====================

A script to allow humans to view a video and log particular events.

Usage:
`python read_video <video_file> <output_file>`

Start time (in seconds) can be controlled with `-t` or `--start-time`.

Starting frame can be controlled with `-f` or `--start-frame`.

e.g. to start 30 seconds into the video, use
`python read_video -t 30 <video_file> <output_file>`

Then follow the instructions onscreen.

Dependencies:

 - OpenCV-Python (install instructions for [windows](http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows) and [fedora linux](http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_fedora/py_setup_in_fedora.html#install-opencv-python-in-fedora))
