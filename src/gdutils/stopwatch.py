########################################################
# from http://effbot.org/librarybook/timing.htm
# File: timing-example-2.py
#
# copied from ~/fmri/distpat/trunk/users/greg/context/time_context.py

"""
This is my wrapper for the time module. There's probably an
easier way to time the duration of things, but when I looked
into timing stuff, this was the best I could come up with...

To use:

    t = Stopwatch()
    # t.start()
    
    # do something

    elapsed = t.finish()
"""

import time


class Stopwatch:
    """
    Creates stopwatch timer objects.
    """

    # stores the time the stopwatch was started
    t0 = None

    # stores the time the stopwatch was last looked at
    t1 = None

    def __init__(self, do_start: bool = True):
        self.t0 = 0
        self.t1 = 0
        if do_start:
            self.start()

    def start(self):
        """
        Stores the current time in t0.
        """

        self.t0 = time.time()

    def finish(self, milliseconds: bool = True):
        """
        Returns the elapsed duration in milliseconds. This
        stores the current time in t1, and calculates the
        difference between t0 (the stored start time) and
        t1, so if you call this multiple times, you'll get a
        larger answer each time.

        You have to call this in order to update t1.
        """

        self.t1 = time.time()
        return self.milli() if milliseconds else self.seconds()

    def seconds(self):
        """
        Returns t1 - t0 in seconds. Does not update t1.
        """
        return int(self.t1 - self.t0)

    def milli(self):
        """
        Returns t1 - t0 in milliseconds. Does not update t1.
        """
        return int((self.t1 - self.t0) * 1000)

    def micro(self):
        """
        Returns t1 - t0 in microseconds. Does not update t1.
        """
        return int((self.t1 - self.t0) * 1000000)
