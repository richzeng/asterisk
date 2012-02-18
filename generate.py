from fingertracker import FingerTracker
import sys
from tracking import util

if __name__ == '__main__':
    f = FingerTracker()
    def run(ti):
        f.run(ti)
    util.produce_to_file(run, sys.argv[1])
