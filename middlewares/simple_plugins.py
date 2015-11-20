import logging
import re

import discord

from core.middleware import Middleware
from core.threads import ThreadWrapper


class SimplePlugins(Middleware):
    '''
    This middleware is recommended for a one server bot or non server specific bot.

    All plugins of the bot will be considered the same on every server.
    '''

    name = 'Simple Plugins'


    def start_all_plugins(self):
        """Starts all the plugins"""

        for plug in self.core.plugins:
            plug['instance'] = plug['plugin'](core=self.core)

    def stop_plugin(self, name):
        """"Stops a particular plugin by its name"""

        for index, plug in enumerate(self.core.plugins):
            if plug['plugin'].name == name:
                if plug['instance'] is not None:
                    self.core.plugins[index]['instance'] = None
                    self.core.plugins[index]['commands'] = []
                    self.core.plugins[index]['rules'] = []
                    self.core.plugins[index]['cron-tasks'] = []
                    return True
                else:
                    logging.debug('Plugin {} not alive.'.format(name))
                    return False
        logging.debug('Plugin {} not found.'.format(name))
        return False

    def start_plugin(self, name):
        """Starts a particular plugin by its name"""

        for index, plug in enumerate(self.core.plugins):
            if plug['plugin'].name == name:
                if plug['instance'] is None:
                    self.core.plugins[index]['instance'] = plug['plugin'](core=self.core)
                    logging.info('Pluging {} alive !'.format(plug['plugin'].name))
                    self.core.load_triggers(plug, 'commands')
                    self.core.load_triggers(plug, 'rules')
                    return True
                else:
                    logging.debug('Plugin {} already alive.'.format(name))
                    return False
        logging.debug('Plugin {} not found.'.format(name))
        return False

    def on_ready(self):
        self.start_all_plugins()

    def require_checker(self, cmd_func, message):
        # check for admin if necessary
        if hasattr(cmd_func, 'require_admin'):
            if message.author.id not in self.core.config['ADMINS']:
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

    def trigger_handler(self, message, plugin):
        isinstance(message, discord.Message)

        # Fetching all the triggers
        trigger_names = [method_name for method_name in dir(plugin) if hasattr(getattr(plugin, method_name),'command') or hasattr(getattr(plugin, method_name),'rule')]
        for trigger_name in trigger_names:

            trigger = getattr(plugin, trigger_name)
            if hasattr(trigger, 'command') and not message.content.startswith(self.core.config['DEFAULT_TRIGGER']):
                continue

            options = re.match(trigger.pattern, message.content[1:])

            if options:
                message.options = options.groups()

                if hasattr(trigger, 'command'):
                    if message.channel.is_private:
                       logging.info('[ PRIVATE MESSAGE ] "{}" from {}'.format(message.content, message.author.name))
                    else:
                       logging.info(
                        '[ CHANNEL MESSAGE ] "{}" from {} in channel {} of server {}'.format(message.content,
                                                                                             message.author.name,
                                                                                             message.channel.name,
                                                                                             message.channel.server.name))
                if not self.require_checker(trigger, message):
                    continue

                if hasattr(trigger, 'thread'):
                    thread = ThreadWrapper(trigger, message)
                    thread.start()
                else:
                    trigger(message)

    def on_message(self, message):
        for plugin in self.core.plugins:
            if plugin['instance']:
                self.trigger_handler(message, plugin['instance'])
