from time import time
from Queue import Empty, Full

class TrackerOut(list):
    """Tracker data output
    """

    def __init__(self, q):
        """Initializes a TrackerOut object

        Arguments:
        :param multiprocessing.Queue q: A FIFO queue to communicate data across
        """
        super(list, self).__init__()
        self.q = q
        self.positions = []

    def flush(self):
        """Reads the most recent data from the tracker input
        """
        try:
            for x in xrange(5):
                pos = self.q.get_nowait()
                self.append(pos)
        except Empty:
            pass

    def clear(self):
        """Clears the list of positions
        """
        del self[0:len(self)-1]

    def time_slice(self, start_time, end_time = None):
        """Returns a list of the finger positions between a given starting time and ending time
        NOT YET IMPLEMENTED

        :param float start_time: A Unix timestamp of the starting time
        :param float end_time: A Unix timestamp of the ending time (default NOW)
        """
        pass


