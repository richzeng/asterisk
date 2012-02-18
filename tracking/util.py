from tracker_in import TrackerIn
from tracker_out import TrackerOut
from time import sleep
from random import randint
from multiprocessing import Queue, Process
from Queue import Empty, Full

def random_producer(ti):
    """A producer that outputs random finger positions

    :param TrackerIn to: A TrackerIn objects that can send data
    """
    while True:
        sleep(0.5)
        t = [ randint(0,100), randint(0,100) ]
        ti.add_positions([t for x in xrange(10)])

def print_consumer(to):
    """A consumer that just prints the finger positions

    :param TrackerOut to: A TrackerOut objects that receives data
    """
    while True:
        to.flush()
        for pos, timestamp in to:
            print "{}: {}".format(int(timestamp), pos)
        to.clear()

def run_async(producer, consumer):
    """Chain a producer and a consumer, running both asyncronously

    :param function producer: A function taking one argument, a TrackerIn
    :param function consumer: A function taking one argument, a TrackerIn
    """
    q = Queue()
    ti = TrackerIn(q)
    to = TrackerOut(q)
    p = Process(target=producer, args=(ti,))
    c = Process(target=consumer, args=(to,))

    c.start()
    p.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        p.terminate()
        c.terminate()
        print "Done"


def run_async_producer(producer, consumer):
    """Chain a producer and a consumer, running the producer asyncronously and the
    consumer in the main thread

    :param function producer: A function taking one argument, a TrackerIn
    :param function consumer: A function taking one argument, a TrackerIn
    """
    q = Queue()
    ti = TrackerIn(q)
    to = TrackerOut(q)
    p = Process(target=producer, args=(ti,))
    p.start()
    try:
        consumer(to)
    except KeyboardInterrupt:
        p.terminate()
        print "Done"

def run_async_consumer(producer, consumer):
    """Chain a producer and a consumer, running the consumer asyncronously and the
    producer in the main thread

    :param function producer: A function taking one argument, a TrackerIn
    :param function consumer: A function taking one argument, a TrackerIn
    """
    q = Queue()
    ti = TrackerIn(q)
    to = TrackerOut(q)
    c = Process(target=consumer, args=(to,))

    c.start()
    try:
        producer(ti)
    except KeyboardInterrupt:
        c.terminate()
        print "Done"
