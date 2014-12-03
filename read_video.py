import cv2
import sys
from getopt import gnu_getopt as getopt
import time

try:
    input = raw_input
except NameError:
    pass


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


def define_event_codes():
    print("Define event codes:")
    event_codes = dict()
    event_frames = dict()
    while True:
        code = input("Enter event code (single lower-case character, or press enter to finish)): ")
        if code is "":
            break
        event_name = input("Enter event name: ")
        event_codes[code] = event_name
        event_frames[ord(code)] = [event_name]

    return event_codes, event_frames


def print_help():
    raise NotImplementedError("I'll implement a help at some point...")


u_args = sys.argv[1:]

optlist, args = getopt(u_args, "t:f:l", ["start-time=", "start-frame=", "help"])
if len(optlist) > 1:
    raise ValueError("Too many optional arguments given: give either a start time or a start frame")

if "--help" in args:
    print_help()
if "-l" in args:
    logical = True

vid_path = args[0]
out_file_path = args[1]

cap = cv2.VideoCapture(vid_path)
vid_fps = cap.get(cv2.CAP_PROP_FPS)

frame_no = 0

if optlist:
    optdict = dict(optlist)
    if "-f" in optdict:
        frame_no = int(optdict["-f"])
    elif "--start-frame" in optdict:
        frame_no = int(optdict["--start_frame"])
    elif "-t" in optdict:
        frame_no = time_to_frame(optdict["-t"])
    elif "--start-time" in optdict:
        frame_no = time_to_frame(optdict["--start-time"])

current_fps = vid_fps

event_codes, event_frames = define_event_codes()

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)    # todo: this might be wrong

print(event_codes)

t = Timer()

while cap.isOpened():
    frame_no += 1

    t.tic()
    _, frame = cap.read()
    cv2.imshow(vid_path, frame)

    inp = cv2.waitKey(round(1000/current_fps - t.toc()*1000))
    if inp is -1:
        continue
    elif inp in event_frames:
        event_frames[inp].append(str(frame_no))
    elif inp is ord(" "):
        break

cap.release()
cv2.destroyAllWindows()

if logical:
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)    # todo: this might be wrong
    for key in event_frames:
        lst = event_frames[key][0] + ['0'] * num_frames
        for frame in event_frames[key][1:]:
            lst[int(frame)] = '1'
        event_frames[key] = lst

events_str = "\n".join([",".join(event_frames[key]) for key in event_frames])

with open(out_file_path, "w") as out_file:
    out_file.write(events_str)