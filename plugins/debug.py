import sys

from core.plugin import Plugin
from core.command import Command
from core.protector import Protector
from core.restricter import Restricter

import discord
import json

from shlex import shlex


class Debug(Plugin):

	name = 'Debug'

	def at_start(self):
		print 'Plugin Debug launched !'

	def on_message(self, message):
		pass#self.evaluate(message)

	def __init__(self, core):
		Plugin.__init__(self, core=core)

		#self.debug = Restricter(channel_id=core.servers[0].channels[3].id)(self.debug)
		#self.debug = Protector(user_ids=['110089625422307328'])(self.debug)

		#self.evaluate = Protector(user_ids=['110089625422307328', '98295630480314368','94129005791281152','86607397321207808'])(self.evaluate)

	'''@Command('eval')
	def evaluate(self, message):
		try:
			e = eval(args[0])
			response = '```python\n'+str(e)+'```'
			self.core.send_message(message.channel, response)
		except:
			e = "Error : "+sys.exc_info()[0].__name__+" \n "+str(sys.exc_info()[1])
			response = '```python\n'+e+'```'
			self.core.send_message(message.channel, response)
			raise'''
