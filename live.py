from gesture import gesture
from fingertracker import FingerTracker

from tracking import util

if __name__ == '__main__':
    f = FingerTracker()
    def run(ti):
        f.run(ti)
    util.run_async_consumer(run, gesture.gesture_consumer)
