import time


class Player(object):
    def __init__(self, member, choice=False, ok=False):
        self.member = member
        self.ok = ok
        self.choice = choice


class Game(object):
    def __init__(self, player1, player2, channel):
        self.players = {
            player1.id: Player(player1, ok=True),
            player2.id: Player(player2),
        }
        self.channel = channel
        self.started = False
        self.capture = False
        self.winner = None

    def start(self, core):
        self.started = True
        self._game_cycle(core)

    def _game_cycle(self, core):
        while not self.winner:
            self.capture = True
            message = "**Please write the corresponding number of your choice !**\n"
            message += "- #0 ROCK\n"
            message += "- #1 PAPER\n"
            message += "- #2 Scisors\n"
            message += "**YOU HAVE 10 SECONDS TO PROVIDE A CHOICE**"
            for pid, player in self.players.items():
                core.send_message(player.member, message=message)
            time.sleep(10)
            for pid, player in self.players.items():
                if not player.choice:
                    message = "{} & {} : One of you didn't respond, game aborted !"
                    core.send_message(self.channel, message)