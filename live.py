from gesture import gesture
from fingertracker import FingerTracker

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

if __name__ == '__main__':
    f = FingerTracker()
    def run(ti):
        f.run(ti)
    util.run_async_consumer(run, gesture_consumer)
