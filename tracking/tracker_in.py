from time import time

class TrackerIn(object):
    """Tracker data input
    """

    def __init__(self, q):
        """Initializes a TrackerIn object

        Arguments:
        :param multiprocessing.Queue q: A FIFO queue to communicate data across
        """
        self.q = q

    def add_positions(self, positions, timestamp=None):
        """Add a set of finger positions

        :param list positions: A list [finger0, ..., finger9] where each finger is a
        tuple [x, y] of the finger's coordinates
        :param float timestamp: Unix timestamp, set as current time if unspecified
        """

        if timestamp is None:
            timestamp = time.now()
        q.put((positions, timestamp))

