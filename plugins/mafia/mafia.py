import time
from threading import Thread
from core.plugin import Plugin
from core.decorators import command, thread, require_chanmsg, rule, require_privmsg
from core.threads import ThreadWrapper
from plugins.mafia.structures import Game, Player


class Mafia(Plugin):
    name = 'Mafia'

    def __init__(self, core):
        Plugin.__init__(self, core=core)
        self.games = {}

    @thread
    @require_chanmsg
    @command('mafia')
    def mafia(self, message):
        # Check if there's already a game
        game = self.games.get(message.channel.id, False)
        if game:
            if game.cycle > 0:
                self.core.send_message(message.author, 'A game is already running in this channel !')
            else:
                if not game.players.get(message.author.id, False):
                    player = Player(message.author, game)
                    game.addplayer(player)
                    announcement = 'Welcome to the game {} ! \n'.format(player.member.mention())
                    self.core.send_message(game.channel, announcement)

        # If there's not
        else:
            # Creating a new game obj
            new_game = Game(message.channel)
            self.games[message.channel.id] = new_game
            player = Player(message.author, game)
            self.games[message.channel.id].addplayer(player)
            # Launching the game create timer in a thread
            timer = self.GameCreatetimer(self._game_create_timer, message.channel)
            timer.start()
            # Announcement
            announcement = "```Hello everyone, let's play a Mafia Game. We need at least 5 players\n"
            announcement += "If you want to play, just type {}mafia in the chat```".format(
                self.core.config['DEFAULT_TRIGGER'])
            self.core.send_message(message.channel, announcement)

    @require_chanmsg
    @command('^nominate <@([0-9]*)>')
    def nominate(self, message):
        game = self.games.get(message.channel.id, False)
        # if game exists
        if not game:
            return False
        player = game.alive_players().get(message.author.id, False)
        # if player in game and alive
        if not player:
            return False
        # if it's nomination time
        if not game.nominate:
            return False
        # if there's a mention
        mention = message.mentions[0] or False
        if not mention:
            return False
        nominated = game.alive_players().get(mention.id, False)
        # if the mention is alive
        if not nominated:
            return False
        game.nominations[player.member.id] = nominated.member.id

    @require_chanmsg
    @command('^kill')
    def vote(self, message):
        game = self.games.get(message.channel.id, False)
        # if game exists
        if not game:
            return False
        player = game.alive_players().get(message.author.id, False)
        # if player in game and alive
        if not player:
            return False
        # if it's nomination time
        if not game.voting:
            return False
        game.votes[player.member.id] = True

    @require_chanmsg
    @rule('(.*)')
    def kill(self, message):
        game = self.games.get(message.channel.id, False)
        # if game exists
        if not game:
            return False
        player = game.alive_players().get(message.author.id, False)
        # if player in game and alive
        if not player:
            return False
        # if it's night
        if game.day:
            return False
        player.alive = False
        self.core.send_message(message.channel,
                               '{} you talked, you are now out of the game ! Bye !'.format(player.member.mention()))

    @require_privmsg
    @rule('^([0-9]*)')
    def pm(self, message):
        games = [self.games[game] for game in self.games if message.author.id in self.games[game].players]
        print(games)
        if games:
            game = games[0]
            print(game)
            if not game.day:
                print('1')
                game.players[message.author.id].pm = message.options[0]
                print(game.players[message.author.id].pm)

    def _game_create_timer(self, channel):
        ttl = 30
        time.sleep(ttl)
        game = self.games[channel.id]
        if game.cycle == 0:
            # if the time is ellapsed
            if len(game.players) < 5:
                del self.games[channel.id]
                announcement = "Not enough players :-( . The game is aborted !"
                self.core.send_message(channel, announcement)
            else:
                announcement = "We found enough players :D ! Time to launch the game !"
                self.core.send_message(channel, announcement)
                game.start(self.core)

    class GameCreatetimer(Thread):
        def __init__(self, f, channel):
            Thread.__init__(self)
            self.f = f
            self.channel = channel

        def run(self):
            self.f(self.channel)
