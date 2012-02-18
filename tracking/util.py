from tracker_in import TrackerIn
from tracker_out import TrackerOut
from time import sleep
from random import randint
from multiprocessing import Queue, Process
from Queue import Empty, Full
import json

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

def file_consumer(filename):
    """A consumer that saves data to a file when you press ctrl-c

    :param string filename: Name of filename to save data in
    """

    f = open(filename, "w")
    def c(to):
        try:
            while True:
                to.flush()
        except KeyboardInterrupt:
            json.dump(to, f)
            f.close()
            print "Done dumping"
    return c

def file_producer(filename):
    """A producer that loads data to a file

    :param string filename: Name of filename to load data from
    """
    f = open(filename, "r")
    l = json.load(f)
    f.close()
    def p(ti):
        while len(l) > 0:
            positions = l.pop(0)
            ti.add_positions(positions)
            sleep(0.5)
    return p

def run_async(producer, consumer):
    """Chain a producer and a consumer, running both asyncronously

    :param function producer: A function taking one argument, a TrackerIn
    :param function consumer: A function taking one argument, a TrackerOut
    """
    q = Queue()
    ti = TrackerIn(q)
    to = TrackerOut(q)
    p = Process(target=producer, args=(ti,))
    c = Process(target=consumer, args=(to,))

    c.start()
    p.start()
    try:
        while c.is_alive() and p.is_alive():
            pass
    except KeyboardInterrupt:
        p.terminate()
        c.terminate()
        print "Done"


def run_async_producer(producer, consumer):
    """Chain a producer and a consumer, running the producer asyncronously and the
    consumer in the main thread

    :param function producer: A function taking one argument, a TrackerIn
    :param function consumer: A function taking one argument, a TrackerOut
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
    :param function consumer: A function taking one argument, a TrackerOut
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

def produce_to_file(producer, filename):
    """Run a producer, save output to a filename after you press Ctrl-C

    :param function producer: A function taking one argument, a TrackerIn
    :param string filename: Name of filename to save data in
    """
    run_async_producer(producer, file_consumer(filename))

def consume_from_file(consumer, filename):
    """Run a producer, save output to a filename after you press Ctrl-C

    :param function consumer: A function taking one argument, a TrackerIn
    :param string filename: Name of filename to load data from
    """
    run_async_consumer(file_producer(filename), consumer)
