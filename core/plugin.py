import logging


class Plugin:
    name = __name__

    def __init__(self, core):
        self.core = core
        self.at_start()
        self.logger = logging.getLogger('robutt')

    def on_message(self, message):
        pass

    def on_ready(self):
        pass

    def at_start(self):
        pass
