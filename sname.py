# -*- coding: utf-8 -*-

import json
import requests

dict = requests.get('https://api.twitch.tv/kraken/channels/tricodin/follows', 'Accept: application/vnd.twitchtv.v3+json')
dict.raise_for_status()

print json.loads(dict.text)