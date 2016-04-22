# -*- coding: utf-8 -*-

from random import randint
import socket
import string
import time
import json
import requests
import login

# Set all the variables necessary to connect to Twitch IRC
MOTD = False
time_counter = time.time()
command_user = []
uses_left = []
mod_list = []
channel_list = ["tricodin"]
colours = ["Blue", "Coral", "DodgerBlue", "SpringGreen", "YellowGreen", "Green", "OrangeRed", "Red", "GoldenRod", "HotPink", "CadetBlue", "SeaGreen", "Chocolate", "BlueViolet", "Firebrick"]
colour_index = 12
 
# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect(("irc.chat.twitch.tv", 80))
s.send("PASS " + login.PASS + "\r\n")
s.send("NICK " + login.NICK + "\r\n")
for c in channel_list:
        s.send("JOIN #" + c + " \r\n")
s.send("CAP REQ :twitch.tv/commands \r\n")
s.settimeout(0.1)


# Method for sending a message
def Send_message(channel, message):
        if channel != "":
                Change_Colour(channel)
                s.send("PRIVMSG #" + channel + " :" + message + "\r\n")
        else:
                global username
                s.send("PRIVMSG #jtv :/w " + username + " " + message + "\r\n")


def Change_Colour(channel):
        global colour_index
        global colours
        colour_index += 1
        if colour_index > 14:
                colour_index = 0
        s.send("PRIVMSG #" + channel + " :/color " + colours[colour_index] + "\r\n")


def Command_used(username):
        global time_counter
        global command_user
        global uses_left
        time_diff = time.time() - time_counter
        
        if time_diff > 300:
                command_user = []
                uses_left = []
        
        if username in command_user:
                i = command_user.index(username)
                if uses_left[i] == 0:
                        return False
                else:
                        uses_left[i] -= 1
                        return True
        else:
                command_user.append(username)
                uses_left.append(4)
                return True


def Set_Game(message):
        if "+" in message:
                message = string.replace(message, "+", "%2B")
        try:
                requests.put('https://api.twitch.tv/kraken/channels/tricodin?oauth_token=' + login.oauth_token + '&Accept=application/vnd.twitchtv.v3+json&channel[game]=' + message)
        except:
                return



def set_title(message):
        if "+" in message:
                message = string.replace(message, "+", "%2B")
        try:
                title = ""
                title_parts = string.split(message, " ")
                for word in title_parts:
                        title = title + word + "+"
                requests.put('https://api.twitch.tv/kraken/channels/tricodin?oauth_token=' + login.oauth_token + '&Accept=application/vnd.twitchtv.v3+json&channel[status]=' + title[:-1])
        except:
                return


def get_mod_list(channel):
        Send_message(channel, "/mods")


def is_permitted(channel, user):
        global mod_list
        global channel_list
        if channel != "":
                i = channel_list.index(channel)
                if user in mod_list[i] or user == channel:
                        return True
                else:
                        return False
        else:
                return False


def receive_message():
        try:
                readbuffer = ""
                readbuffer = readbuffer + s.recv(1024)
                temp = string.split(readbuffer, "\n")
                readbuffer = temp.pop()
        except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                        return ""
                else:
                        print e
                        sys.exit(1)
        except socket.error, e:
                print e
                sys.exit(1)
        else:
                return temp
                
while True:
        temp = receive_message()
        if temp == "":
                continue
        else:
                print temp
                for line in temp:
                        # Checks whether the message is PING because its a method of Twitch to check if you're afk
                        if (line[:4] == "PING"):
                                s.send("PONG tmi.twitch.tv\r\n")
                        else:
                                # Splits the given string so we can work with it better
                                parts = string.split(line, ":")
                                
                                if "NOTICE" in parts[1] and "moderators" in parts[2]:
                                        mod_list.append(string.split(parts[3][1:-1], ", "))
                                if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1] and "USERSTATE" not in parts[1] and "NOTICE" not in parts[1]:
                                        try:
                                                # Sets the message variable to the actual message sent
                                                message = ':'.join(parts[2:])
                                                message = message[:-1]
                                        except:
                                                message = ""
                                        # Sets the username variable to the actual username
                                        usernamesplit = string.split(parts[1], "!")
                                        username = usernamesplit[0]
                                        
                                        if "WHISPER" in parts[1]:
                                                channel = ""
                                        else:
                                                for c in channel_list:
                                                        if "#" + c in parts[1]:
                                                                channel = c
                       
                                        # Only works after twitch is done announcing stuff (MODT = Message of the day)
                                        if MOTD:
                                                print username + ": " + message
                            
                                                # You can add all your plain commands here
                                                if "!roll" in message[:5].lower():
                                                        if Command_used(username):
                                                                if message.lower() == "!roll":
                                                                        Send_message(channel, username + " rolled " + str(randint(1, 20)) + "!")
                                                                else:
                                                                        try:
                                                                                dice = string.split(message, "d")
                                                                                dNum = dice[0][5:]
                                                                                dSize = dice[1]
                                                                                dNum = int(dNum)
                                                                                dSize = int(dSize)
                                                                                if dNum > 10 or dSize > 100:
                                                                                        Send_message(channel, "Too big. Max is 10 dice or 100 sides.")
                                                                                else:
                                                                                        total_rolled = 0
                                                                                        rolled_out = "! ("
                                                                                        for i in range(0, dNum):
                                                                                                rolled_num = randint(1, dSize)
                                                                                                total_rolled = total_rolled + rolled_num
                                                                                                rolled_out = rolled_out + str(rolled_num) + " + "
                                                                                        if dNum == 1:
                                                                                                Send_message(channel, username + " rolled " + str(total_rolled) + "!")
                                                                                        else:
                                                                                                Send_message(channel, username + " rolled " + str(total_rolled) + rolled_out[:-3] + ")")
                                                                        except:
                                                                                message = ""
                                                '''
                                                if message[:5].lower() == "!time":
                                                        if Command_used(username):
                                                                time_split = string.split(message, " ")
                                                                try:
                                                                        if time_split[1] == "r":
                                                                                print "shit"
                                                        
                                                                        if message.lower() == "!time":
                                                                                clock = time.strftime("%H:%M:%S", time.localtime(time.time()))
                                                                                clock = string.split(clock, ":")
                                                                                phours = int(clock[0])
                                                                                pmin = int(clock[1]) + (60 * phours)
                                                                                psec = int(clock[2]) + (60 * pmin)
                                                                                pclock = psec / 864.0
                                                                                pclock = '%.2f' % round(pclock, 2)
                                                                                Send_message(channel, "It is " + pclock + "%")
                                                                        elif message.lower() == "!timepst":
                                                                                clock = time.strftime("%H:%M:%S", time.localtime(time.time()))
                                                                                clock = string.split(clock, ":")
                                                                                phours = int(clock[0])
                                                                                pmin = int(clock[1]) + (60 * phours)
                                                                                psec = int(clock[2]) + (60 * pmin)
                                                                                pclock = (psec - 16200) % 86400
                                                                                pclock = pclock / 864.0
                                                                                pclock = '%.2f' % round(pclock, 2)
                                                                                Send_message(channel, "It is " + pclock + "%")
                                                
                                                if message.lower() == "!test":
                                                        if Command_used(username):
                                                                target = open(var/www/tricbot.me/html/trash.html, 'w')
                                                                target.truncate()
                                                                target.write("done")
                                                                Send_message(channel, "done")
                                                '''
                                                                
                                                if message.lower() == "!orb":
                                                        if Command_used(username):
                                                                Send_message(channel, "🔮")    
                                                                
                                                if message.lower() == "!wr":
                                                        if Command_used(username):
                                                                Send_message(channel, "٩( ᐛ )و WR ٩( ᐛ )و ")
                                                     
                                                if message.lower() == "!penguin":
                                                        if Command_used(username):
                                                                Send_message(channel, "ᕕ( ' >' )ᕗ")
                                                                        
                                                if message[:5].lower() == "!game":
                                                        Set_Game(message[6:])
                                                        
                                                if message[:6].lower() == "!title":
                                                        set_title(message[7:])
         
                                        for l in parts:
                                                if "twitch.tv/commands" in l and not MOTD:
                                                        MOTD = True
                                                        for c in channel_list:
                                                                        get_mod_list(c)