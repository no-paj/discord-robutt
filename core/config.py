from ..middlewares import simple_plugins


ADMINS = [
    '110089625422307328',
    '94129005791281152',
    '112592601865072640',
    '94978269052407808',
    '86607397321207808',
    '105635576866156544'
]

DEFAULT_TRIGGER = '+'

config = {
    'ADMINS': ADMINS,
    'DEFAULT_TRIGGER': DEFAULT_TRIGGER,
    'DATABASE': 'database.db',
    'MIDDLEWARES':[
        simple_plugins.SimplePlugins
                   ]
}
