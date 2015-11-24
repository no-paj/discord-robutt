mafia_roles = []


def mafia_role(cls):
    def classret():
        return cls

    mafia_roles.append(cls)
    return classret


@mafia_role
class Cop(object):
    name = 'Cop'
    help_text = "A killer for the side of the villagers."
    ratio = 1 / 7.
    return_id = "cop"
    mafia = False


@mafia_role
class Doctor(object):
    name = 'Doctor'
    help_text = "An innocent who may protect a player from being killed every night."
    ratio = 1 / 7.
    return_id = "doc"
    mafia = False


@mafia_role
class Barman(object):
    name = 'Barman'
    help_text = "A mafioso who may cancel the effect of another role's ability every night."
    ratio = 1 / 7.
    return_id = "bar"
    mafia = True


@mafia_role
class Mafioso(object):
    name = 'Mafioso'
    help_text = "A member of the mob who can Kill every night."
    ratio = 1 / 4.5
    return_id = "maf"
    mafia = True


@mafia_role
class Villager(object):
    name = 'Villager'
    help_text = "A regular villager."
    ratio = 0
    return_id = "vil"
    mafia = False


def generate_roles(players):
        player_assignments = [role() for role in mafia_roles if role.ratio!= 0 for i in range(int(max(1, role.ratio*players)))]
        player_assignments.extend([mafia_roles[-1]() for v in range(players - len(player_assignments))])
        return player_assignments