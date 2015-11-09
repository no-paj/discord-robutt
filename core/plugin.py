class Plugin:

	name = __name__

	def __init__(self, core):
		self.core = core
		self.at_start()

	def on_message(self, message):
		pass

	def at_start(self):
		pass
