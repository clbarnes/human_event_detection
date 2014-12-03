Human event detection
=====================

## DEPENDENCIES

 - OpenCV-Python (install instructions for [windows](http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows) and [fedora linux](http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_fedora/py_setup_in_fedora.html#install-opencv-python-in-fedora))

## SYNOPSIS

`python read_video [options] VIDEO_PATH OUTPUT_PATH`

## DESCRIPTION

A script to allow humans to view a video and log particular events.

When the script is run, the user can specify keypresses which correspond to the identification of any number of different types of event. The user then watches the video, logging events as it plays (press `Space` to quit). The frames during which events were logged is then written to a CSV. If the `-l` flag is used, the CSV contains a logical array of event frames rather than a list of linear indices.

## OPTIONS

`-f NUM, --start-frame=NUM`
Frame number at which to start video playback

`-t SECONDS, --start-time=SECONDS`
Time at which to start video playback 

`--help`
Not yet implemented

`-l`
Return event frames as logical array rather than list of frame numbers

## BUGS

See the [issue tracker](https://github.com/clbarnes/human_event_detection/issues).

## AUTHOR

Chris Barnes < cbarnes@mrc-lmb.cam.ac.uk >