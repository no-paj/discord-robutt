from time import time
import discord
import core.config


class Core(discord.Client):
    """Represents the core of the Bot. Extends from discord.Client
	This class is used to add a plugin layer and a database layer to discord.Client

	:param list plugins: A list of plugins

	"""

    def __init__(self, **kwargs):
        discord.Client.__init__(self, **kwargs)
        self.start_time = time()
        self.config = core.config.config
        self.plugins = [
            {
                'instance': None,
                'plugin': plugin,
                'commands': []
            } for plugin in kwargs.get('plugins')
            ]

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
                    return True
                else:
                    print('Plugin {} not alive.'.format(name))
                    return False
        print('Plugin {} not found.'.format(name))
        return False

    def start_plugin(self, name):
        """Starts a particular plugin by its name"""

        for index, plug in enumerate(self.plugins):
            if plug['plugin'].name == name:
                if plug['instance'] is None:
                    self.plugins[index]['instance'] = plug['plugin'](core=self)
                    return True
                else:
                    print('Plugin {} already alive.'.format(name))
                    return False
        print('Plugin {} not found.'.format(name))
        return False

    def load_commands(self):
        """Loads all the cmd of a plugin"""
        for plugin in self.plugins:
            if plugin['instance']:
                for func_name in dir(plugin['instance']):
                    if callable(getattr(plugin['instance'], func_name)):
                        func = getattr(plugin['instance'], func_name)
                        if hasattr(func, 'command'):
                            require_admin = False
                            require_chanmsg = False
                            require_privmsg = False
                            example = ''
                            if hasattr(func, 'require_admin'):
                                require_admin = True
                            if hasattr(func, 'require_privmsg'):
                                require_privmsg = True
                            if hasattr(func, 'require_chanmsg'):
                                require_chanmsg = True
                            if hasattr(func, 'example'):
                                example = func.example
                            cmd = {
                                'name': func_name,
                                'require_admin': require_admin,
                                'require_privmsg': require_privmsg,
                                'require_chanmsg': require_chanmsg,
                                'example': example,
                                'description': func.__doc__,
                            }
                            plugin['commands'].append(cmd)
                            print('{} command loaded !'.format(func_name))

    def run_time(self):
        """Give the run time of the instance

		:return: A :int: in seconds
		"""
        return time() - self.start_time

    def on_ready(self):
        """Called when the client is running and is ready"""
        self.start_all_plugins()
        self.load_commands()

    def on_message(self, message):
        """Called whenever a message is posted

		:param message: The message that is posted
		"""

        for plugin in self.plugins:
            if plugin['instance']:
                for command in plugin['commands']:
                    command_func = getattr(plugin['instance'], command['name'])
                    run = '1'
                    if hasattr(command_func, 'require_admin'):
                        if message.author.id not in self.config['ADMINS']:
                            continue
                    if hasattr(command_func, 'require_privmsg'):
                        if not message.channel.is_private:
                            continue
                    if hasattr(command_func, 'require_chanmsg'):
                        if message.channel.is_private:
                            continue

                    command_func(message)
