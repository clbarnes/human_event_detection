import cv2
import sys
from getopt import gnu_getopt as getopt
from ConfigParser import ConfigParser


DEFAULT_CONFIG = "config.conf"

def time_str_to_frame(seconds_str):
    seconds = float(seconds_str)
    return round(seconds*vid_fps)


def initialise_event_frames(config_file_path=DEFAULT_CONFIG):
    conf = ConfigParser()
    conf.read([config_file_path])
    return {ord(key): [value] for value, key in conf.items("event key mappings")}


def get_property_keys(config_file_path=DEFAULT_CONFIG):
    conf = ConfigParser()
    conf.read([config_file_path])
    return {key: int(value) for key, value in conf.items("openCV property keys")}


def print_help():
    raise NotImplementedError("I'll implement a help at some point...")


u_args = sys.argv[1:]

optlist, args = getopt(u_args, "t:f:lc:s:", ["help"])

if ("--help", "") in optlist:
    print_help()
    sys.exit()

if optlist:
    optdict = dict(optlist)

    if "--help" in optdict:
        print_help()
        sys.exit()

    logical = "-l" in optdict

    config_file = optdict.get("-c", DEFAULT_CONFIG)

    vid_speed = float(optdict.get("-s", 1))

    if "-f" in optdict:
        frame_no = int(optdict["-f"])
    elif "-t" in optdict:
        frame_no = time_str_to_frame(optdict["-t"])
    else:
        frame_no = 0
else:
    logical = False
    config_file = DEFAULT_CONFIG
    vid_speed = 1
    frame_no = 0

vid_path = args[0]
out_file_path = args[1]

openCV_properties = get_property_keys(config_file)

cap = cv2.VideoCapture(vid_path)
vid_fps = cap.get(openCV_properties["fps"])
num_frames = cap.get(openCV_properties["frame_count"])

event_frames = initialise_event_frames(config_file)

def pause(arg):
    cv2.waitKey(0)

def speed_up(delay):
    return delay - (1000/vid_fps)*0.1

def slow_down(delay):
    return delay + (1000/vid_fps)*0.1

def initialise_playback_controls(config_file_path):
    conf = ConfigParser()
    conf.read([config_file_path])
    name_to_value = {key: ord(value) for key, value in conf.items("playback key mappings")}
    playback_controls = {
        name_to_value["pause"]: pause,
        name_to_value["speed_up"]: speed_up,
        name_to_value["slow_down"]: slow_down
    }
    return playback_controls


playback_controls = initialise_playback_controls(config_file)

cap.set(openCV_properties["position_frames"], frame_no)

delay = int(round(1000/(vid_fps*vid_speed)))
while cap.isOpened():
    frame_no += 1

    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow(vid_path, frame)

    inp = cv2.waitKey(delay)
    if inp is -1:
        continue
    elif inp in event_frames:
        event_frames[inp].append(str(frame_no))
    elif inp is ord(" "):
        break

cap.release()
cv2.destroyAllWindows()


if logical:
    for key in event_frames:
        lst = [event_frames[key][0]] + ['0'] * int(num_frames)
        for frame in event_frames[key][1:]:
            lst[int(frame)] = '1'
        event_frames[key] = lst

events_str = "\n".join(sorted([",".join(event_frames[key]) for key in event_frames]))

with open(out_file_path, "w") as out_file:
    out_file.write(events_str)