from threading import Thread
import time


class CronWrapper(Thread):

    def __init__(self, f, seconds):
        Thread.__init__(self)
        self.f = f
        self.seconds = seconds

    def run(self):
        while True:
            self.f()
            time.sleep(self.seconds)