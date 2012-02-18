"""Visualize a stored gesture file"""
import sys
from tracking import util

if __name__ == '__main__':
    util.visualize_file(sys.argv[1])
