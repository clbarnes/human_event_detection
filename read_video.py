import cv2
import sys
from getopt import gnu_getopt as getopt
import time


def time_to_frame(seconds_str):
    seconds = float(seconds_str)
    return round(seconds*vid_fps)


class Timer():
    def __init__(self):
        self.start_time = None
        if sys.platform == 'win32':
            self.default_timer = time.clock
        else:
            self.default_timer = time.time

    def tic(self):
        self._manual_start_time = self.default_timer()

    def toc(self):
        return self.default_timer() - self._manual_start_time

    def __enter__(self):
        self.start_time = self.default_timer()
        return self

    def __exit__(self, *args):
        self.end_time = self.default_timer()
        self.interval = self.start_time - self.end_time


def print_help():
    raise NotImplementedError("I'll implement a help at some point...")


u_args = sys.argv[1:]

optlist, args = getopt(u_args, "t:f:", ["start-time=", "start-frame=", "help"])
if len(optlist) > 1:
    raise ValueError("Too many optional arguments given: give either a start time or a start frame")

if "--help" in args:
    print_help()

vid_path = args[0]
out_file_path = args[1]

cap = cv2.VideoCapture(vid_path)
vid_fps = cap.get(cv2.CAP_PROP_FPS)

start_frame = 0

if optlist:
    optdict = dict(optlist)
    if "-f" in optdict:
        start_frame = int(optdict["-f"])
    elif "--start-frame" in optdict:
        start_frame = int(optdict["--start_frame"])
    elif "-t" in optdict:
        start_frame = time_to_frame(optdict["-t"])
    elif "--start-time" in optdict:
        start_frame = time_to_frame(optdict["--start-time"])

current_fps = vid_fps

events = []
frame_no = 0
while frame_no < start_frame and cap.isOpened():    # todo: something better than this!
    frame_no += 1
    _, frame = cap.read()

t = Timer()

while cap.isOpened():
    frame_no += 1

    t.tic()
    _, frame = cap.read()
    cv2.imshow('frame', frame)

    inp = cv2.waitKey(round(1000/current_fps - t.toc()*1000))
    if inp is -1:
        continue
    elif inp is ord(" "):
        events.append(frame_no)
    elif inp is ord("d"):
        events.pop()
    elif inp is ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

events_str = "\n".join([str(event) for event in events])

with open(out_file_path, "w") as out_file:
    out_file.write(events_str)