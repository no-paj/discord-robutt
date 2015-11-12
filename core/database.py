import logging

from peewee import *
from playhouse.db_url import connect
from playhouse.kv import JSONKeyStore


class User(Model):
    name = CharField()
    discord_id = CharField(unique=True)
    discriminator = CharField()
    avatar = CharField(null=True)
    avatar_url = CharField(null=True)


class Server(Model):
    name = CharField()
    region = CharField()
    icon = CharField(null=True)
    discord_id = CharField(unique=True)
    owner = ForeignKeyField(User)


class Channel(Model):
    name = CharField()
    server = ForeignKeyField(Server, null=True)
    discord_id = CharField(unique=True)
    topic = CharField(null=True)
    is_private = BooleanField(null=True)
    position = CharField(null=True)
    type = CharField()


class Message(Model):
    edited_timestamp = DateTimeField()
    timestamp = DateTimeField()
    tts = BooleanField(null=True)
    author = ForeignKeyField(User)
    content = TextField()
    channel = ForeignKeyField(Channel,null=True)


class Database:
    """
    Thanks ZETA ;)
    """
    def __init__(self, database):
        self.connection = connect(database)
        self.connection.connect()
        self.keystore = JSONKeyStore(database=self.connection)
        self.logger = logging.getLogger('robutt')

    def add_table(self, table):
        setattr(table._meta, 'database', self.connection)
        setattr(self, table.__name__, table)
        table.create_table(table)
        self.logger.info('Table {} loaded !'.format(table.__name__))

    def add_tables(self, tables):
        for table in tables:
            self.add_table(table)
