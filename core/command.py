import discord
import re
from core.config import config
from functools import wraps


class command:
    def __init__(self, pattern, trigger=config['DEFAULT_TRIGGER']):

        self.pattern = pattern
        self.trigger = trigger

    def __call__(self, f):

        @wraps(f)
        def wrapped(core, msg):
            assert isinstance(msg, discord.Message)
            if msg.content:
                if msg.content[0] == self.trigger:
                    options = re.match(self.pattern, msg.content[1:])
                    if options:
                        options = options.groups()
                        msg.options = options
                        f(core, msg)

        wrapped.command = True
        return wrapped
