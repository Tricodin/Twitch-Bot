# -*- coding: utf-8 -*-

import json
import requests

dict = requests.get('https://api.twitch.tv/kraken/channels/tricodin/follows', 'Accept: application/vnd.twitchtv.v3+json')
dict.raise_for_status()
result = json.loads(dict.text)
i = 0
while (True):
        try:
                print result['follows'][i]['user']['name']
                i += 1
        except:
                break


