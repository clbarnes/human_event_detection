human_event_detection
=====================

A script to allow humans to view a video and log particular events.

Usage:
`python read_video <video_file> <output_file>`
Start time (in seconds) can be controlled with `-t` or `--start-time`.
Starting frame can be controlled with `-f` or `--start-frame`.
e.g. to start 30 seconds into the video, use
`python read_video -t 30 <video_file> <output_file>`

Dependencies:
 - OpenCV-Python (install instructions for windows and fedora linux)
