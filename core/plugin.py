class Plugin:

	def __init__(self, name, core):
		self.name = name
		self.core = core
		self.at_start()

	def on_message(self, message):
		pass

	def at_start(self):
		pass
