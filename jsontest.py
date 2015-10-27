# -*- coding: utf-8 -*-

import json
import requests
from urllib import urlopen

file = "followers.txt"
offsetCounter = 0
resultIndex = 0
followersLeft = True
target = open(file, 'w')


target.truncate()
while(followersLeft):
        try:
                url = urlopen('https://api.twitch.tv/kraken/channels/tricodin/follows?direction=DESC&limit=100&offset=' + str(offsetCounter) ).read()
                result = json.loads(url)
                offsetCounter += 100
                for i in range(0, 100):
                        target.write(result['follows'][i]['user']['name'])
                        target.write('\n')
        except:
                followersLeft = False
                
target.close()

for i in range (0, 5):
        recent = open(file, 'r')
        print recent.readline()
        recent.close()