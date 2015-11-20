import re
from time import time
import discord
import core.config
import logging
import core.database
from core import database
from core.threads import ThreadWrapper
from peewee import *


# TODO HANDLE ALL OTHER EVENTS

class Core(discord.Client):
    """Represents the core of the Bot. Extends from discord.Client
    This class is used to add a plugin layer and a database layer to discord.Client

    :param list plugins: A list of plugins

    """

    def __init__(self, **kwargs):
        discord.Client.__init__(self, **kwargs)
        self.logger = logging.getLogger('robutt')
        self.start_time = time()
        self.config = kwargs.get('conf')
        self.middlewares = self.config['MIDDLEWARES']
        self.logger.info('Configuration loaded.')
        self.plugins = [
            {
                'plugin': plugin,
                'instance': None,
            } for plugin in kwargs.get('plugins')
            ]
        self.logger.info('Plugin(s) loaded.')

        self.database = database.Database(database='sqlite:///database.db')
        self.database.add_tables([
            database.Server,
            database.Channel,
            database.User,
            database.Message
        ])

        self._load_middlewares()

    def _load_middlewares(self):
        ''' Loading all middlewares '''
        for index, middleware in enumerate(self.middlewares):
            self.middlewares[index] = middleware(core=self)

    def run_time(self):
        """Give the run time of the instance

        :return: A :int: in seconds
        """
        return time() - self.start_time

    def on_ready(self):
        """Called when the client is running and is ready"""

        for middleware in self.middlewares:
            middleware.on_ready()


    def on_message(self, message):
        """Called whenever a message is posted

        :param message: The message that is posted
        """
        for middleware in self.middlewares:
            middleware.on_message(message)
