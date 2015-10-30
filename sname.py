# -*- coding: utf-8 -*-

import json
import requests

#gttkgjljwcvgr410yttc3aouq8jkim
thing = json.loads('{"channel": {"status": "If I can see this, it worked", "game": "Diablo"}}')
print thing
dict = requests.put('https://api.twitch.tv/kraken/channels/tricodin?oauth_token=486z221swxbmqar075ef26anzi90aw&Accept=application/vnd.twitchtv.v3+json&channel[status]=Playing+cool+new+game!&channel[game]=Diablo')
dict.raise_for_status()
result = json.loads(dict.text)

print result


#https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=otiybjr5kz95ibw0z0vm0quc1notfys&redirect_uri=http://localhost&scope=channel_read+channel_editor