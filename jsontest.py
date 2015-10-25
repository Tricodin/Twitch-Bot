# -*- coding: utf-8 -*-

import json
import requests
from urllib import urlopen

url = urlopen('https://api.twitch.tv/kraken/channels/tricodin/follows?direction=DESC&limit=1&offset=104').read()
result = json.loads(url)


print result['follows'][0]['user']['name']