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
        self.logger.info('Configuration loaded.')
        self.plugins = [
            {
                'plugin': plugin,
                'instance': None,
                'commands': [],
                'rules': [],
                'cron-tasks': [],
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

    def start_all_plugins(self):
        """Starts all the plugins"""

        for plug in self.plugins:
            plug['instance'] = plug['plugin'](core=self)

    def stop_plugin(self, name):
        """"Stops a particular plugin by its name"""

        for index, plug in enumerate(self.plugins):
            if plug['plugin'].name == name:
                if plug['instance'] is not None:
                    self.plugins[index]['instance'] = None
                    self.plugins[index]['commands'] = []
                    self.plugins[index]['rules'] = []
                    self.plugins[index]['cron-tasks'] = []
                    return True
                else:
                    logging.debug('Plugin {} not alive.'.format(name))
                    return False
        logging.debug('Plugin {} not found.'.format(name))
        return False

    def start_plugin(self, name):
        """Starts a particular plugin by its name"""

        for index, plug in enumerate(self.plugins):
            if plug['plugin'].name == name:
                if plug['instance'] is None:
                    self.plugins[index]['instance'] = plug['plugin'](core=self)
                    logging.info('Pluging {} alive !'.format(plug['plugin'].name))
                    self.load_triggers(plug, 'commands')
                    self.load_triggers(plug, 'rules')
                    return True
                else:
                    logging.debug('Plugin {} already alive.'.format(name))
                    return False
        logging.debug('Plugin {} not found.'.format(name))
        return False

    def load_triggers(self, plugin, type):
        """Loads all the cmd of a plugin"""
        logging.info('[ Loading {} of {} ]'.format(type, plugin['plugin'].name))
        if plugin['instance']:
            for func_name in dir(plugin['instance']):
                func = getattr(plugin['instance'], func_name)
                if callable(func):
                    singular_type = type[:-1]
                    if hasattr(func, singular_type):
                        require_admin = False
                        require_chanmsg = False
                        require_privmsg = False
                        example = ''
                        require_owner = False
                        require_botcom = False
                        interval = None
                        if hasattr(func, 'require_admin'):
                            require_admin = True
                        if hasattr(func, 'require_privmsg'):
                            require_privmsg = True
                        if hasattr(func, 'require_chanmsg'):
                            require_chanmsg = True
                        if hasattr(func, 'require_owner'):
                            require_owner = True
                        if hasattr(func, 'require_botcom'):
                            require_botcom = True
                        if hasattr(func, 'example'):
                            example = func.example
                        if hasattr(func, 'interval'):
                            interval = func.interval
                        trigger = {
                            'name': func_name,
                            'require_admin': require_admin,
                            'require_privmsg': require_privmsg,
                            'require_chanmsg': require_chanmsg,
                            'require_botcom': require_botcom,
                            'require_owner': require_owner,
                            'example': example,
                            'description': func.__doc__,
                            'interval': {
                                'delay': interval,
                                'records': []
                            },
                        }
                        plugin[type].append(trigger)
                        logging.info('{} {} loaded !'.format(func_name, type))

    def load_all_triggers(self, type):
        """Loads all the triggers of a type  of all plugins"""
        for plugin in self.plugins:
            self.load_triggers(plugin, type)

    def run_time(self):
        """Give the run time of the instance

        :return: A :int: in seconds
        """
        return time() - self.start_time

    def require_checker(self, cmd_func, message):
        # check for admin if necessary
        if hasattr(cmd_func, 'require_admin'):
            if message.author.id not in self.config['ADMINS']:
                logging.info(
                    '[ NOT AN ADMIN ] {} is not an admin !'.format(message.author.name))
                return False
        # check for pvmessage if necessary
        if hasattr(cmd_func, 'require_privmessage'):
            if not message.channel.is_private:
                logging.info('[ REQUIRE PV ] last msg from {} requires PV !'.format(
                    message.author.name))
                return False
        # check for chanmsg if necessary
        if hasattr(cmd_func, 'require_chanmessage'):
            if message.channel.is_private:
                logging.info(
                    '[ REQUIRE CHAN ] last msg from {} requires CHAN !'.format(
                        message.author.name))
                return False
        # check for owner if necessary
        if hasattr(cmd_func, 'require_owner'):
            if message.author is message.channel.server.owner:
                logging.info(
                    '[ NOT AN OWNER ] {} is not owner of {} !'.format(message.author.name, message.channel.server.name))
                return False
        # check for botcom
        if hasattr(cmd_func, 'require_owner'):
            if 'Bot Commander' in [r for r in map(lambda r:r.name, message.author.roles)]:
                logging.info(
                    '[ NOT A BOTCOM ] {} is not the botcom of {} !'.format(message.author.name,
                                                                           message.channel.server.name))
                return False
        # if all is good
        return True

    def on_ready(self):
        """Called when the client is running and is ready"""
        self.start_all_plugins()
        self.load_all_triggers('commands')
        self.load_all_triggers('rules')

    def on_message(self, message):
        """Called whenever a message is posted

        :param message: The message that is posted
        """

        # Handling plugin commands
        ###### if message is a command
        if message.content.startswith(self.config['DEFAULT_TRIGGER']):
            # Logging
            if message.channel.is_private:
                self.logger.info('[ PRIVATE MESSAGE ] "{}" from {}'.format(message.content, message.author.name))
            else:
                self.logger.info(
                    '[ CHANNEL MESSAGE ] "{}" from {} in channel {} of server {}'.format(message.content,
                                                                                         message.author.name,
                                                                                         message.channel.name,
                                                                                         message.channel.server.name))
            for plugin in self.plugins:

                # If plugin active !
                if plugin['instance']:
                    # If yes then :
                    # Fetching the commands
                    for command in plugin['commands']:
                        cmd_func = getattr(plugin['instance'], command['name'])
                        options = re.match(cmd_func.pattern, message.content[1:])
                        # check for pattern validation and required specificities
                        if options and self.require_checker(cmd_func, message):
                            options = options.groups()
                            message.options = options
                            # Check if thread func
                            if hasattr(cmd_func, 'thread'):
                                thread = ThreadWrapper(cmd_func, message)
                                thread.start()
                            else:
                                cmd_func(message)

        # Handling plugin rules
        for plugin in self.plugins:
            if plugin['instance']:

                # If yes then :
                # Fetching all the rules
                for rule in plugin['rules']:
                    rule_func = getattr(plugin['instance'], rule['name'])
                    options = re.match(rule_func.pattern, message.content)
                    if options and self.require_checker(rule_func, message):
                        options = options.groups()
                        message.options = options
                        # Check if thread func
                        if hasattr(rule_func, 'thread'):
                            thread = ThreadWrapper(rule_func, message)
                            thread.start()
                        else:
                            rule_func(message)
