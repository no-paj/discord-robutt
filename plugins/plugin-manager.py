from core.plugin import Plugin
from core.command import Command


class PluginManager(Plugin):

	name = 'Plugin-manager'

	def __init__(self, core):
		Plugin.__init__(self, core)

	def on_message(self, message):
		self.plugin_list(message)

	@Command('plugin-list')
	def plugin_list(self, message):
		for plug in self.core.plugins:
			response = plug['plugin'].name
			if plug['instance'] is not None:
				response += ' | Running'
			self.core.send_message(message.channel, response)