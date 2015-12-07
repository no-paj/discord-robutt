import time

import discord

from core.plugin import Plugin
from core.decorators import command, cron


class Reminder(Plugin):
    name = 'Reminder'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command(
        '^remind (me|<@[0-9]*>) to (.*) in ((([0-9]*)( )?(hours|hour))?( )?(([0-9]*)( )?(minutes|minute))?( )?(([0-9]*)( )?(seconds|second))?)')
    def remind(self, message):
        to_who = message.author.id
        if message.options[0] != 'me':
            if not message.mentions:
                return False
            to_who = message.mentions[0].id
        to = message.options[1]
        hour = int(message.options[4] or 0)
        minutes = int(message.options[9] or 0)
        seconds = int(message.options[14] or 0)

        reminder_time = time.time() + (seconds + minutes * 60 + hour * 3600)
        self.core.db.reminders.insert_one({
            'user_id': message.author.id,
            'to_who_id': to_who,
            'to': to,
            'time': reminder_time
        })
        print(time.time()-reminder_time)
        subject = 'you'
        if to_who != message.author.id:
            subject = message.mentions[0].mention()

        ok_message = '{}, I\'ll remind {} to "{}" in "{}" ;) !'.format(
            message.author.mention(),
            subject,
            to,
            message.options[2],
            str(reminder_time)
        )

        self.core.send_message(message.channel, ok_message)

    @cron(1)
    def remind_checker(self):
        to_remind = self.core.db.reminders.find({
            'time': {
                '$lt': time.time()
            }
        })
        for reminder in to_remind:
            user = discord.utils.find(lambda m: m.id == reminder['user_id'],
                                      [member for server in self.core.servers for member in server.members])
            send_to = user
            subject = 'You'
            if reminder['to_who_id'] != reminder['user_id']:
                send_to = discord.utils.find(lambda m: m.id == reminder['to_who_id'],
                                      [member for server in self.core.servers for member in server.members])
                subject = user.mention()
            msg = '{} told me to remind you to **"{}"** !\n Job done ! ;)'.format(
                subject,
                reminder['to']
            )

            self.core.send_message(send_to, msg)
            self.core.db.reminders.delete_many({
                '_id': reminder['_id']
            })

