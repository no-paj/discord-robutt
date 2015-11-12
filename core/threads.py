from threading import Thread


class ThreadWrapper(Thread):

    def __init__(self, f, msg):
        Thread.__init__(self)
        self.f = f
        self.msg = msg

    def run(self):
        self.f(self.msg)

