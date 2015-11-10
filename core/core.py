from time import time

import discord
import config


class Core(discord.Client):
	"""Represents the core of the Bot. Extends from discord.Client
	This class is used to add a plugin layer and a database layer to discord.Client

	:param list plugins: A list of plugins

	"""

	def __init__(self, **kwargs):
		discord.Client.__init__(self, **kwargs)
		self.start_time = time()
		self.config = config.config
		self.plugins = [
			{
				'instance': None,
				'plugin': plugin,
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
					print 'Plugin {} not alive.'.format(name)
					return False
		print 'Plugin {} not found.'.format(name)
		return False

	def start_plugin(self, name):
		"""Starts a particular plugin by its name"""

		for index, plug in enumerate(self.plugins):
			if plug['plugin'].name == name:
				if plug['instance'] is None:
					self.plugins[index]['instance'] = plug['plugin'](core=self)
					return True
				else:
					print 'Plugin {} already alive.'.format(name)
					return False
		print 'Plugin {} not found.'.format(name)
		return False

	def run_time(self):
		"""Give the run time of the instance

		:return: A :int: in seconds
		"""
		return time() - self.start_time

	def on_ready(self):
		"""Called when the client is running and is ready"""
		self.start_all_plugins()

		for plug in self.plugins:
			if plug['instance']:
				plug['instance'].on_ready()

	def on_message(self, message):
		"""Called whenever a message is posted

		:param message: The message that is posted
		"""

		for plug in self.plugins:
			if plug['instance']:
				plug['instance'].on_message(message)
