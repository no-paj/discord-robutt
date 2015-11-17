import logging

import discord


class Middleware(object):

    name = __name__

    def __init__(self, core):
        self.core = core
        self.logger = logging.getLogger('robutt')
        logging.info('[ Initialising Middleware {} ]'.format(self.name))

    def on_ready(self):
        pass

    def on_message(self, message):
        pass

    def on_message_delete(self, message):
        pass

    def on_message_edit(self, before, after):
        pass

    def on_status(self, member):
        pass

    def on_channel_delete(self, channel):
        pass

    def on_channel_create(self, channel):
        pass

    def on_channel_update(self, channel):
        pass

    def on_member_join(self, member):
        pass

    def on_member_update(self, member):
        pass

    def on_server_create(self, server):
        pass

    def on_server_delete(self, server):
        pass

    def on_server_role_create(self, server, role):
        pass

    def on_server_role_delete(self, server, role):
        pass

    def on_server_role_update(self, server, role):
        pass

    def on_voice_state_update(self, member):
        pass

    def on_socket_opened(self):
        pass

    def on_socket_closed(self):
        pass

    def on_socket_update(self, event, data):
        pass

    def on_socket_response(self, response):
        pass

    def on_socket_raw_receive(self, msg):
        pass

    def on_socket_raw_send(self, payload, binary=False):
        pass
