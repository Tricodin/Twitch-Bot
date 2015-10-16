# -*- coding: utf-8 -*-

from random import randint
import socket, string
import time
 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "tricbot"
PORT = 6667
PASS = "oauth:uu4byfxrxg5n9odpzxzvsl9tt3oa78"
readbuffer = ""
MODT = False
time_counter = time.time()
command_user = []
uses_left = []
colours = ["Blue", "Coral", "DodgerBlue", "SpringGreen", "YellowGreen", "Green", "OrangeRed", "Red", "GoldenRod", "HotPink", "CadetBlue", "SeaGreen", "Chocolate", "BlueViolet", "Firebrick"]
colour_index = 12
 
# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #tricodin \r\n")
 
# Method for sending a message
def Send_message(message):
	s.send("PRIVMSG #tricodin :" + message + "\r\n")
        
def Change_Colour():
        global colour_index
        global colours
        colour_index = colour_index + 1
        if colour_index > 14:
                colour_index = 0
        Send_message("/color " + colours[colour_index])
        
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
                
 
 
while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()
 
        for line in temp:
                # Checks whether the message is PING because its a method of Twitch to check if you're afk
                if (line[:4] == "PING"):
                        s.send("PONG tmi.twitch.tv\r\n")
                else:
                        # Splits the given string so we can work with it better
                        parts = string.split(line, ":")
 
                        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                                try:
                                        # Sets the message variable to the actual message sent
                                        message = parts[2][:len(parts[2]) - 1]
                                except:
                                        message = ""
                                # Sets the username variable to the actual username
                                usernamesplit = string.split(parts[1], "!")
                                username = usernamesplit[0]
               
                                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                                if MODT:
                                        print username + ": " + message
                    
                                        # You can add all your plain commands here
                                        if "!roll" in message or "Roll" in message:
                                                if Command_used(username):
                                                        if message == "!roll" or message == "!Roll":
                                                                Change_Colour()
                                                                Send_message(username + " rolled " + str(randint(1, 20)) + "!")
                                                        elif message[:5] == "!roll":
                                                                try:
                                                                        dice = string.split(message, "d")
                                                                        dNum = dice[0][5:]
                                                                        dSize = dice[1]
                                                                        dNum = int(dNum)
                                                                        dSize = int(dSize)
                                                                        if dNum > 10 or dSize > 100:
                                                                                Change_Colour()
                                                                                Send_message("Too big. Max is 10 dice or 100 sides.")
                                                                        else:
                                                                                total_rolled = 0
                                                                                rolled_out = "! ("
                                                                                for i in range(0, dNum):
                                                                                        rolled_num = randint(1, dSize)
                                                                                        total_rolled = total_rolled + rolled_num
                                                                                        rolled_out = rolled_out + str(rolled_num) + " + "
                                                                                Change_Colour()
                                                                                Send_message(username + " rolled " + str(total_rolled) + rolled_out[:-3] + ")")
                                                                except:
                                                                        message = ""
                                                                
                                        if "brett" in message or "Brett" in message:
                                                if "bretty" not in message and "Bretty" not in message:
                                                        Change_Colour()
                                                        Send_message("I think you mean BrettySuzy, " + username)
                                                        
                                        if message == "!WR" or message == "!wr":
                                                if Command_used(username):
                                                        Change_Colour()
                                                        Send_message("٩( ᐛ )و WR ٩( ᐛ )و ")
                                             
                                        if message == "!penguin" or message == "!Penguin":
                                                if Command_used(username):
                                                        Change_Colour()
                                                        Send_message("ᕕ( ' >' )ᕗ")
 
                                for l in parts:
                                        if "End of /NAMES list" in l:
                                                MODT = True