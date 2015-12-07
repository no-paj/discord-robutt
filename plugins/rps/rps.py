import time
from threading import Thread
from core.plugin import Plugin
from core.decorators import command, thread, require_chanmsg, rule, require_privmsg
from core.threads import ThreadWrapper
from plugins.rps.structures import Game


class Rps(Plugin):
    name = 'RPS'

    def __init__(self, core):
        Plugin.__init__(self, core=core)
        self.games = {}

    @require_chanmsg
    @command('(rps) <@[(0-9]*)>')
    def rps(self, message):
        if not message.mentions:
            return False
        if self.games[message.author.id]:
            return False

        players = [message.author, message.mentions[0]]
        timer = self.GameCreatetimer(self._game_create_timer(players, message.channel))
        timer.run()

    @thread
    @require_chanmsg
    @command('^(ok)')
    def ok(self, message):
        game = self._get_player_game(message.author)
        # if user not in a game
        if not game:
            return False
        # if game started
        if game.started:
            return False
        if game.players[message.author.id].ok:
            return False
        game.players[message.author.id].ok = True
        game.start()

    @require_privmsg
    @command('(.*)')
    def capture(self, message):
        game = self._get_player_game(message.author)
        # if user not in a game
        if not game:
            return False
        # if the game isnt in capture mode
        if not game.capture:
            return False
        if 0 <= int(message.content) < 3:
            game.players[message.author.id].choice = int(message.content)

    def _get_player_game(self, player):
        for game in self.games:
            if player.id in game.players:
                return game
        return False

    def _game_create_timer(self, players, channel):
        self.games[players[0].id] = Game(players[0], players[1], channel)
        game = self.games[players[0].id]
        ttl = 30
        time.sleep(ttl)
        if not game.started:
            del self.games[players[0].id]
            message = "{}, game aborted. {} didn't respond :-( .".format(players[0].mention(), players[1].mention())
            self.core.send_message(channel, message)

    class GameCreatetimer(Thread):
        def __init__(self, f, channel):
            Thread.__init__(self)
            self.f = f
            self.channel = channel

        def run(self):
            self.f(self.channel)
