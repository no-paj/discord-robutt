import discord


class Middleware(object):

    name = __name__

    def __init__(self, core):
        self.core = core
