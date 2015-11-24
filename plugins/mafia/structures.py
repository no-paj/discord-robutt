from random import shuffle

import time

from plugins.mafia.roles import generate_roles, mafia_roles


class Player:
    def kill(self):
        self.alive = False

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def __init__(self, member, game, role=None, alive=True, blocked=False):
        self.member = member
        self.game = game
        self.role = role
        self.alive = alive
        self.blocked = blocked
        self.protected = False
        self.pm = -1


class Game:
    def addplayer(self, player):
        self.players[player.member.id] = player

    def start(self, core):
        if len(self.players) > 4:
            self.cycle = 1
            self._game_cycle(core)

    def __init__(self, channel):
        self.channel = channel
        self.cycle = 0
        self.voting = False
        self.nominate = False
        self.nominations = {}
        self.votes = {}
        self.day = True
        self.players = {}
        self.nominee_id = ''
        self.log = ''

    def _game_cycle(self, core):
        while self.cycle != 0:
            if self.day and self.cycle == 1:
                roles = generate_roles(len(self.players))
                self._give_roles(roles)
                self._tell_roles(core)
                self._tell_welcome_message(core)
                time.sleep(10)

            if self._end_game():
                self.cycle = 0
                continue

            if self.day:
                self._announcement_day(core, 60)
                self._nomination(core, 30)
                self._nomination_results(core, 20)
                self._voting(core, 30)

            if not self.day:
                message = 'The night came !\n'
                message += '**No one is allowed to talk here !**\n'
                message += 'If you talk, you get killed !'
                core.send_message(self.channel, message)
                self._night_handle(core, 60)
        message = '**This is the end of the game my friends !**\n'
        message += ' The {} won !\n'.format(self._end_game())
        message += 'Here are the survivors:**\n'
        for k,v in self.alive_players().items():
            message += '- {} ({}) \n'.format(v.member.mention(), v.role.name)
        core.send_message(self.channel, message)

    def _end_game(self):
        alive = self.alive_players()
        mafia = False
        village = False
        for pid in alive:
            if self.players[pid].role.mafia == True:
                mafia = True
            else:
                village = True
        if mafia==True and village==True:
            return False
        else:
            if mafia==True:
                return 'mafia'
            else:
                return 'village'

    def _give_roles(self, roles):
        shuffle(roles)
        for player_id in self.players:
            self.players[player_id].role = roles[0]
            del roles[0]

    def _tell_roles(self, core):
        for player_id in self.players:
            player = self.players[player_id]
            message = "Hello {} ! Let's play !\n".format(player.member.name)
            message += "I see that you are a {} !\n".format(player.role.name)
            message += "Description of your role :```{}```".format(player.role.help_text)
            core.send_message(player.member, message)
            if player.role.mafia:
                message = "It seems that you are part of the mob !\n"
                message += "Here is your team my friend : \n"
                for pid in self.players:
                    p = self.players[pid]
                    if p.role.mafia and pid != player_id:
                        message += "- **{}** / role : {}\n".format(p.member.name, p.role.name)
                core.send_message(player.member, message)

    def _tell_welcome_message(self, core):
        message = "Hello Fellows !\n\n"
        message += "Here is the list of people playing the game ! \n"
        for player_id in self.players:
            player = self.players[player_id]
            message += '- {} \n '.format(player.member.mention())
        message += "\n**A brief recall of the game roles :** \n"
        for role in mafia_roles:
            message += "{} : *{}*\n".format(role.name, role.help_text)
        message += '\n Good game and have fun ! ;)'
        core.send_message(self.channel, message)

    def _announcement_day(self, core, pause):
        message = "This is the day number {} my friends !\n".format(str(self.cycle))
        if self.log!='':
            message+="\n"
            message+= '**What happened last night :** \n'
            message+=self.log
        self.log = ''
        message += "\nHere are the players that are still alive ! \n"
        message += self.log
        self.log = ''
        for pid in self.alive_players():
            player = self.alive_players()[pid]
            message += "- {} \n".format(player.member.mention())
        message += "I give you {} seconds to discuss about what's going on.".format(str(pause))
        core.send_message(self.channel, message)
        time.sleep(pause)

    def alive_players(self):
        players = {}
        for player_id in self.players:
            player = self.players[player_id]
            if player.alive:
                players[player_id] = player
        return players

    def _nomination(self, core, pause):
        message = "It's time to nominate someone my friends !\n"
        message += "Here are the people that you can nominate : \n"
        for pid in self.alive_players():
            player = self.alive_players()[pid]
            message += "- {} \n".format(player.member.mention())
        message += "To nominate someone, just type `{}nominate @player` !\n".format(core.config['DEFAULT_TRIGGER'])
        message += "You have {} seconds.".format(str(pause))
        self.nominate = True
        core.send_message(self.channel, message)
        time.sleep(pause)

    def _get_nomination_score(self):
        score = {}
        for player, nominated in self.nominations.items():
            if score.get(nominated, False):
                score[nominated] += 1
            else:
                score[nominated] = 1
        return score, sorted(score, key=score.get, reverse=True)


    def _nomination_results(self, core, pause):
        self.nominate = False
        if self.nominations == {}:
            message = "No one was nominated today !"
            core.send_message(self.channel, message)
            self.day = False
            return False
        message = "Here are the nomination results !\n"
        core.send_message(self.channel, message)
        time.sleep(2)
        score, sorted_score = self._get_nomination_score()
        if len(sorted_score) > 1:
            if score[sorted_score[0]] == score[sorted_score[1]]:
                message = "It's a tie between {} and {} at least !\n".format(self.players[sorted_score[0]].member.mention(),self.players[sorted_score[1]].member.mention())
                message += "No nomination today !"
                core.send_message(self.channel, message)
                self.day = False
                return False
        self.nominee_id = sorted_score[0]
        message = " The nominee is : {} !\n".format(self.players[sorted_score[0]].member.mention())
        message += "You have {} seconds to defend yourself before the vote !".format(str(pause))
        core.send_message(self.channel, message)
        self.nominations = {}
        time.sleep(pause)

    def _voting(self, core, pause):
        if self.nominee_id != '':
            message = "It's time to vote my friends !"
            message += "If you want to kill {}, type `{}kill` !\n".format(self.players[self.nominee_id].member.mention(), core.config['DEFAULT_TRIGGER'])
            message += "You have {} seconds.".format(str(pause))
            core.send_message(self.channel, message)
            self.voting = True
            time.sleep(pause)
            self.voting = False
            message = "It's time for the vote results !\n"
            core.send_message(self.channel, message)
            time.sleep(1)
            message = "{} votes against {} !".format(len(self.votes), self.players[self.nominee_id].member.mention())
            core.send_message(self.channel, message)
            time.sleep(2)
            if len(self.votes) > len(self.alive_players())/2:
                message = "{} is killed !".format(self.players[self.nominee_id].member.mention())
                self.players[self.nominee_id].alive = False
            else:
                message = "Not enough votes. {} is still alive !".format(self.players[self.nominee_id].member.mention())
            core.send_message(self.channel, message)
            time.sleep(1)
            self.nominee_id = ''
            self.votes = {}
            message = "End of the day..."
            core.send_message(self.channel, message)
            self.day = False

    def _night_handle(self, core, pause):
        alive_players = self.alive_players()
        alive_players_list = list(alive_players)
        for pid in alive_players:
            player = alive_players[pid]
            if player.role.name == 'Cop' or player.role.name == 'Mafioso':
                message = 'This night, you can kill some one if you want.\n'
                message += 'Type a number if you want to kill the corresponding player.\n'
                for index, player_id in enumerate(alive_players_list):
                    message += '**#{}** : {}\n'.format(str(index), alive_players[player_id].member.name)
                core.send_message(player.member, message)
            if player.role.name == 'Barman':
                message = 'This night, you can cancel an effect of any player.\n'
                message += 'Type a number if you want to block the corresponding player.\n'
                for index, player_id in enumerate(alive_players_list):
                    message += '**#{}** : {}\n'.format(str(index), alive_players[player_id].member.name)
                core.send_message(player.member, message)
            if player.role.name == 'Doctor':
                message = 'This night, you can protect a player\n'
                message += 'Type a number if you want to protect the corresponding player.\n'
                for index, player_id in enumerate(alive_players_list):
                    message += '**#{}** : {}\n'.format(str(index), alive_players[player_id].member.name)
                core.send_message(player.member, message)
        time.sleep(pause)
        # BARMAN BLOCK
        for pid in alive_players:
            player = self.players[pid]
            if player.pm != '':
                pm = int(player.pm)
                if 0 <= pm < len(alive_players_list):
                    if player.role.name == 'Barman':
                        player.pm = ''
                        self.players[alive_players_list[pm]].blocked = True
                        message = 'You woke up completly drunk today !'
                        core.send_message(self.players[alive_players_list[pm]].member, message)
        # DOCTOR
        for pid in alive_players:
            player = self.players[pid]
            if player.pm != '':
                pm = int(player.pm)
                if 0 <= pm < len(alive_players_list):
                    if player.role.name == 'Doctor' and player.blocked == False:
                        player.pm = ''
                        self.players[alive_players_list[pm]].protected = True
        # COP AND MAFIOSO
        for pid in alive_players:
            player = self.players[pid]
            if player.pm != '':
                pm = int(player.pm)
                if 0 <= pm < len(alive_players_list):
                    if player.role.name in ['Cop', 'Mafioso'] and player.blocked == False:
                        player.pm = ''
                        if not self.players[alive_players_list[pm]].protected:
                            self.players[alive_players_list[pm]].alive = False
                            self.log += '{} was killed, he was a {} !\n'.format(self.players[alive_players_list[pm]].member.mention(), self.players[alive_players_list[pm]].role.name)
                        if self.players[alive_players_list[pm]].protected:
                            message = 'Someone tried to kill you tonight ! You should thank the doctor for having saved you !'
                            core.send_message(self.players[alive_players_list[pm]].member, message)

        for pid in alive_players:
            player = alive_players[pid]
            player.blocked = False
            player.protected = False

        self.day = True
        self.cycle += 1




