from time import time
from Queue import Empty, Full

class TrackerOut(list):
    """Tracker data output
    """

    def __init__(self, q):
        """Initializes a TrackerOut object

        :param multiprocessing.Queue q: A FIFO queue to communicate data across
        """
        super(list, self).__init__()
        self.q = q
        self.positions = []

    def flush(self):
        """Reads the most recent data from the tracker input
        """
        try:
            for x in xrange(100):
                pos = self.q.get_nowait()
                self.append(pos)
            else:
                print "WARNING: did not flush fully"
        except Empty:
            pass

    def clear(self):
        """Clears the list of positions
        """
        del self[0:len(self)]

    def time_slice(self, start_time, end_time = None):
        """Returns a list of the finger positions between a given starting time and ending time

        :param float start_time: A Unix timestamp of the starting time
        :param float end_time: A Unix timestamp of the ending time (default NOW)
        """
        if end_time is None:
            end_time = self[-1][1]
        i = len(self) - 1
        while 0 < i and end_time < self[i][1]:
            i -= 1

        end_index = i + 1

        while 0 < i and start_time < self[i][1]:
            i -= 1

        start_index = i
        if self[start_index][1] < start_time:
            start_index += 1

        if start_index == len(self):
            return []
        else:
            return self[start_index:end_index]
