from gesture import gesture
import sys

import tracking
from tracking import util

def gesture_consumer(to):
    MAX_POINTS = 150
    most_recent = 0
    while True:
        to.flush()
        if len(to) > MAX_POINTS:
            del to[:-MAX_POINTS]
        if len(to) > 2:
            if most_recent != to[-1][1]:
                most_recent = to[-1][1]
                g = gesture.match(gesture.gestures, map(lambda x: x[0], to))
                if g != None:
                    g.execute()
                else:
                    print "No gesture found"

def run_from_file(filename):
    util.consume_from_file(gesture_consumer, filename)

if __name__ == '__main__':
    run_from_file(sys.argv[1])
