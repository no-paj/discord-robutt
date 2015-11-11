import discord
import re
from core.config import config
from functools import wraps


class Command:
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


def thread(f):
    f.thread = True
    return f


def require_privmsg(f):
    f.require_privmsg = True
    return f


def require_chanmsg(f):
    f.require_chanmsg = True
    return f


def require_admin(f):
    f.require_admin = True
    return f


class Example:
    def __init__(self, text):
        self.text = text

    def __call__(self, f):
        f.example = self.text
        return f
