import sys

from core.plugin import Plugin
from core.decorators import Command
from core.protector import Protector
from core.restricter import Restricter

import discord
import json

from shlex import shlex


class Debug(Plugin):

	name = 'Debug'

	def at_start(self):
		print('Plugin Debug launched !')

	def on_message(self, message):
		self.evaluate(message)
		self.get_cid(message)
		self.get_uid(message)

	def __init__(self, core):
		Plugin.__init__(self, core=core)

		self.evaluate = Protector(user_ids=core.config['ADMINS'])(self.evaluate)
		self.get_cid = Protector(user_ids=core.config['ADMINS'])(self.get_cid)
		self.get_uid = Protector(user_ids=core.config['ADMINS'])(self.get_uid)

	@Command('^eval (.*)$')
	def evaluate(self, message):
		try:
			e = eval(message.options[0])
			response = '```python\n'+str(e)+'```'
			self.core.send_message(message.channel, response)
		except:
			e = "Error : "+sys.exc_info()[0].__name__+" \n "+str(sys.exc_info()[1])
			response = '```python\n'+e+'```'
			self.core.send_message(message.channel,  "```\shell\n{}```".format(__import__('traceback').format_exc()))
			raise

	@Command('^uid <@([0-9]*)>')
	def get_uid(self, message):
		self.core.send_message(message.channel, "{}'s UID :  `{}`".format("<@{}>".format(message.options[0]), message.options[0]))

	@Command('^cid <#([0-9]*)>')
	def get_cid(self, message):
		self.core.send_message(message.channel, "{}'s CID :  `{}`".format("<#{}>".format(message.options[0]), message.options[0]))
