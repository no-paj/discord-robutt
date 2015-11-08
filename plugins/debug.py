import sys

from core.plugin import Plugin
from core.command import Command
from core.protector import Protector
from core.restricter import Restricter

import discord
import json

from shlex import shlex


class Debug(Plugin):

	def at_start(self):
		print 'Plugin Debug launched !'

	def on_message(self, message):
		self.debug(message)
		self.evaluate(message)

	def __init__(self, core):
		Plugin.__init__(self, name='Debug', core=core)

		self.debug = Restricter(channel_id=core.servers[0].channels[3].id)(self.debug)
		self.debug = Protector(user_ids=['110089625422307328'])(self.debug)

		self.evaluate = Protector(user_ids=['110089625422307328', '98295630480314368','94129005791281152','86607397321207808'])(self.evaluate)

	@Command('eval', startswith=True)
	def evaluate(self, message, args):
		try:
			e = eval(args[0])
			response = '```python\n'+str(e)+'```'
			self.core.send_message(message.channel, response)
		except:
			e = "Error : "+sys.exc_info()[0].__name__+" \n "+str(sys.exc_info()[1])
			response = '```python\n'+e+'```'
			self.core.send_message(message.channel, response)
			raise

	@Command('debug')
	def debug(self, message):
		assert isinstance(message, discord.Message)
		response = '```json\n'+json.dumps(self._info(message), indent=4, sort_keys=True) + '```'
		self.core.send_message(message.channel, response)

	def _info(self, obj):
		info = {}
		if isinstance(obj, discord.Message):
			info = {
				'type': 'Message',
				'author': self._info(obj.author),
				'content': obj.content.encode('utf-8'),
				'channel': self._info(obj.channel)
			}
		if isinstance(obj, discord.User):
			info = {
				'type': 'User',
				'name': obj.name.encode('utf-8'),
				'user_id': obj.id,
			}
		if isinstance(obj, discord.Channel):
			info = {
				'type': 'Channel',
				'name': obj.name.encode('utf-8'),
				'id': obj.id
			}

		return info