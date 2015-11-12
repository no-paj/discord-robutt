from core.plugin import Plugin
from core.decorators import command


class PluginManager(Plugin):

    name = 'Plugin-manager'

    def __init__(self, core):
        Plugin.__init__(self, core)

    @command('^plugin-list$')
    def plugin_list(self, message):
        response = ''
        for plug in self.core.plugins:
            response += plug['plugin'].name
            if plug['instance'] is not None:
                response += ' | Running'
            else:
                response += ' | NOT running'
            response += " \n"
        self.core.send_message(message.channel, '```\n' + response + '```')

    @command('^plugin-stop ([A-Za-z]+)$')
    def plugin_stop(self, message):
        if self.core.stop_plugin(message.options[0]):
            self.core.send_message(message.channel, '```{} Stopped !```'.format(message.options[0]))
        else:
            self.core.send_message(message.channel, '```A problem occured... :(```')

    @command('^plugin-start ([A-Za-z]+)$')
    def plugin_start(self, message):
        if self.core.start_plugin(message.options[0]):
            self.core.send_message(message.channel, '```{} Started !```'.format(message.options[0]))
        else:
            self.core.send_message(message.channel, '```A problem occured... :(```')
