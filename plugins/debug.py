import sys
from core.plugin import Plugin
from core.decorators import command, example, require_privmsg, require_admin


class Debug(Plugin):
    name = 'Debug'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @require_admin
    @command('^eval (.*)$')
    @example('{}eval 1+1')
    def evaluate(self, message):
        '''Self-made backdoor!!!'''
        try:
            e = eval(message.options[0])
            response = '```python\n' + str(e) + '```'
            self.core.send_message(message.channel, response)
        except:
            e = "Error : " + sys.exc_info()[0].__name__ + " \n " + str(sys.exc_info()[1])
            response = '```python\n' + e + '```'
            self.core.send_message(message.channel, "```\shell\n{}```".format(__import__('traceback').format_exc()))
            raise

    @command('^uid <@([0-9]*)>')
    @example('{}uid @User')
    def get_uid(self, message):
        '''Get a user id'''
        self.core.send_message(message.channel,
                               "{}'s UID :  `{}`".format("<@{}>".format(message.options[0]), message.options[0]))

    @command('^cid <#([0-9]*)>')
    @example('{}cid @Channel')
    def get_cid(self, message):
        '''Get a channel id'''
        self.core.send_message(message.channel,
                               "{}'s CID :  `{}`".format("<#{}>".format(message.options[0]), message.options[0]))

    @require_admin
    @command('^save (users|server|all)$')
    def save(self, message):
        """Save all users or all channels of the server or both"""
        if message.options[0] == 'users':
            self.core.database.User.insert_many(
                [
                    {
                        'name': user.name,
                        'discord_id': user.id,
                        'discriminator': user.discriminator,
                        'avatar': user.avatar,
                        'avatar_url': user.avatar_url(),
                    } for user in message.channel.server.members
                ]
            ).on_conflict(action='REPLACE').execute()
        # TODO FINISH THE SAVE CMD


