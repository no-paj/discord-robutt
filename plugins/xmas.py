import os
import time
from base64 import b64encode
from threading import Thread
from core.plugin import Plugin
from core.decorators import command, thread, require_chanmsg, rule, require_privmsg, require_admin
from core.threads import ThreadWrapper
from plugins.rps.structures import Game
from PIL import Image as Image
from io import BytesIO as BytesIO
import requests
from imgurpython import ImgurClient


class Xmas(Plugin):
    name = 'Xmas'


    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('^xmas|xmas <@([0-9]*)>')
    def xmas(self, message):
        client_id = '7d5a48eb8f3b168'

        headers = {"Authorization": "Client-ID "+client_id}

        api_key = 'f2886ec020ea9c5a46141bf8d6d7e100c2bc1bb1'

        url = "https://api.imgur.com/3/upload.json"
        if message.mentions:
            user = message.mentions[0]
        else:
            user = message.author
        ava = BytesIO(requests.get(user.avatar_url()).content)
        img = Image.open(ava)
        foreground = Image.open('hathat.png')
        img.paste(foreground, (0, 0), foreground)
        img.save('ava.jpg')

        j1 = requests.post(
            url,
            headers=headers,
            data={
                'key': api_key,
                'image': b64encode(open('ava.jpg', 'rb').read()),
                'type': 'base64',
                'name': 'ava.jpg',
                'title': 'Discord XMAS !!!!'
            }
        )

        os.remove('ava.jpg')
        self.core.send_message(message.channel, j1.json()['data']['link'])
