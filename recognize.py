from gesture import gesture
import sys

import tracking
from tracking import util

def run_from_file(filename):
    util.consume_from_file(gesture.gesture_consumer, filename)

if __name__ == '__main__':
    run_from_file(sys.argv[1])
