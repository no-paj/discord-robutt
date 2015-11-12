def command(pattern):
    """Make a function a command that follow the given regex pattern.

    It will capture groups and store them into the array message.options

    :param pattern:
    :return: a command function
    """
    def wrapped(f):
        f.command = True
        f.pattern = pattern
        return f
    return wrapped


def rule(pattern):
    """Make a function following a regex rule given in the pattern string

    It will trigger the function every-time the pattern is respected

    :param pattern:
    :return: a rule function
    """
    def wrapped(f):
        f.rule = True
        f.pattern = pattern
        return f
    return wrapped


def thread(f):
    """Make a function executed in a separate Thread

    :param f:
    :return: a function that will be executed in a separate Thread
    """
    f.thread = True
    return f


def require_privmsg(f):
    """Make a function be triggered when private messaging

    :param f: the function
    :return: a function to be triggered when private messaging
    """
    f.require_privmsg = True
    return f


def require_chanmsg(f):
    """Make a function be triggered when channel messaging

    :param f: the function
    :return: a function to be triggered when channel messaging
    """
    f.require_chanmsg = True
    return f


def require_admin(f):
    """Make a function admin protected !

    :param f:
    :return: a function admin protected
    """
    f.require_admin = True
    return f


def example(text):
    """Give to a function the example stored in string text. Usefull for the !help command for example.

    :param text:
    :return: a function with an example text
    """
    def wrapped(f):
        f.example = text
        return f
    return wrapped
