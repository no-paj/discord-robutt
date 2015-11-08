from core.plugin import Plugin
from core.command import Command
from random import randint

import discord
import requests


class Boobs(Plugin):

	def at_start(self):
		print 'Plugin Boobs launched !'

	def on_message(self, message):
		self.boobs(message)

	def __init__(self, core):
		Plugin.__init__(self, name='Boobs', core=core)

	@Command('boobs')
	def boobs(self, message):
		assert isinstance(message, discord.Message)
		response = self._get_boobs()
		self.core.send_message(message.author, response)

	def _get_boobs(self):
		boobs = []
		while not boobs:
			boobs = requests.get('http://api.oboobs.ru/boobs/get/'+str(randint(42, 9500))).json()
		return 'http://media.oboobs.ru/'+boobs[0]['preview']