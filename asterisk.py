"""Asterisk main executable"""
import sys

from fingertracker import FingerTracker
from gesture import gesture
from tracking import util

def run():
    f = FingerTracker()
    def producer(ti):
        f.run(ti)
    util.run_async_consumer(producer, gesture.gesture_consumer)

def dump(filename):
    f = FingerTracker()
    def run(ti):
        f.run(ti)
    util.produce_to_file(run, filename)

def visualize(filename):
    util.visualize_file(filename)

def runfile(filename):
    util.consume_from_file(gesture.gesture_consumer, filename)

def main():
    if len(sys.argv) == 1:
        print """usage: python asterisk.py command [filename]

Commands are:
  run         Run Asterisk finger tracking and gesture recognition
  dump        Run Asterisk finger tracking, and dump the resulting data to disk
              (requires filename argument)
  visualize   Visualize finger positions from a data file
              (requires filename argument)
  runfile     Run Asterisk gesture recognition on a finger postions file
              (requires filename argument)
"""
    elif (sys.argv[1] == 'run'):
        run()
    else:
        if len(sys.argv) < 2:
            print "Error: filename parameter required"
        elif sys.argv[1] == 'dump':
            dump(sys.argv[2])
        elif sys.argv[1] == 'visualize':
            visualize(sys.argv[2])
        elif sys.argv[1] == 'runfile':
            runfile(sys.argv[2])
        else:
            print "Error: unknown command '{}'".format(sys.argv[1])

if __name__ == '__main__':
    main()
