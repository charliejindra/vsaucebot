#!/usr/bin/python3.7
import tweepy as tp      # twitter api
import time
import datetime          # datetime class
import random            # rng
import pytz              # python timezones

#NOTE : as of now streaming stuff doesn't work with this file, although the skeleton is still here. It is functioning on streamMichel.py


#myStream.filter(track=['vsauce', 'vsauce bot', '@vsaucebot', 'Michael Stevens'], async=True)

#spaceOut function
def spaceOut(oldString): # takes string as input, returns string with spaces inserted at every capital letter
    pos = 0
    newString = ''
    while pos < len(oldString):
        newString = newString + oldString[pos]  # add letter from old to new

        try:
            if ((oldString[pos + 1].isupper()) and (pos != 0) and (oldString[pos] != ' ') and ((not oldString[pos+2].isupper()) or oldString[pos].islower())) and (not(oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].isupper())) or (oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].islower()) or (oldString[pos+1].isupper() and oldString[pos+2:].islower()):
                # if the next letter is capital
                # and not at the 0th position (so we dont have a space at the beginning)
                # and we're not at a space (so we dont have double spaces)
                # and 2 characters from now we dont have an uppercase (to check if we're in the middle of an acronym or something thats all caps)
                # OR (in a new branch) if this character and the last one were capital, and the next one is lowercase (end of an acronym)
                # OR (in a new branch) if this character is capital but every character after isnt
                newString = newString + ' '    # add space to new string
        except:   # when it gets to end of string it goes here, this is probably sloppy as hell
            time.sleep(0)

        pos = pos + 1
    return newString

#twitter API credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#login to twitter account as:
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)
print('running!')
#actual twitter stuff yay
i = 0; # just here to create infinite loop

#creating stream for replies and likes
#overriding mystreamlistener to add logic to on_status
class MyStreamListener(tp.StreamListener):
    def on_status(self, status):
        if not status.user.screen_name == "vsaucebot":
            api.create_favorite(status.id)

#actually making stream
myStreamListener = MyStreamListener()
myStream = tp.Stream(auth = api.auth, listener=myStreamListener)

#incrementing the log number
runNo = open("logs/runNo.txt", 'r') # open runNo in r to read number its on
currentNo = int(runNo.read())
runNo.close()
runNo = open("logs/runNo.txt", 'w') # open runNo in w to write the incremented v on it
currentNo = currentNo + 1
runNo.write(str(currentNo))    # now writing the new number to runNo
runNo.close()

# bitstring to keep track of which sayings have been used
wasUsedList = []
michelSayings = open("michelSayings.txt", 'r', encoding="utf8")
for cnt, line in enumerate(michelSayings):     # make the bitstring the length of michel sayings, each bit corresponds to a line in michelSayings.txt
    wasUsedList.append(False) # false means it hasn't been used yet
print("length of michelSayings bitstring: " + str(len(wasUsedList))) # print length of michel bit
michelSayings.close()
trueAmount = 0 # the amount of "True"s in the bitstring. I increment it along the way, this way we don't have to check the whole bs every time

# makin a new log each time yea boi
exeLog = open("logs/log"+str(currentNo)+".txt", 'w+') # create new log for this edition yaye, w+ makes new file
print("Started Log #"  + str(currentNo))

while i < 1:
    print('-----------------')
    now = datetime.datetime.now(pytz.timezone('America/New_York')) # sets the timezone to new york so its not britain yay
    exeLog.write("Started Log #"  + str(currentNo))
    exeLog.write(str(now)  + "\n")
    message = ""
    trends1 = api.trends_place(23424977) # grab trends from United States
    # trends1 is a list with only one element in it, which is a
    # dict which we'll put in data.
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    # put all the names together with a ' ' separating them
    trendsName = ' '.join(names)

    trendNo = random.randint(1, 48) #random trend from 1st to 50th
    while ("Thoughts" in trends[trendNo]["name"]): # if its some dumbass shit like sunday thoughts then we're not using it
         trendNo = random.randint(1, 48) #random trend from 1st to 50th
    exeLog.write(str(trendNo) + "\n")

    useTrend = trends[trendNo]["name"]     #trend to use
    wasHashtag = False
    if (useTrend[0] == '#'):
        wasHashtag = True
    useTrend = useTrend.strip("#")
    if (not useTrend.isupper()) : # if its all caps or wasnt a hashtag just keep it, don't space out  //and (not wasHashtag)
        useTrend = spaceOut(oldString = useTrend)
    isPlural = False
    if useTrend.endswith('s') :
        isPlural = True

    fp = open("michelSayings.txt", 'r', encoding="utf8") # open michelSayings.txt in plaintext

    while True:              # basically a do while loop
        lineNo = random.randint(0, 97) # pick random line number from michelSayings
        print("the number was " + str(lineNo))
        if not(wasUsedList[lineNo]):# as long as the line number has not been used, then break, otherwise loop again
            wasUsedList[lineNo] = True  # now set it to true
            trueAmount = trueAmount + 1
            exeLog.write("\ntrueAmount = " + str(trueAmount)+ "\n")
            print("trueAmount = " + str(trueAmount))
            break

    #check if theres enough "True"s to reset the bitstring
    if trueAmount > len(wasUsedList)/3:     # 1/3 of the sayings have to have been used in the bitstring before it resets and lets you use whatever again
        #reset bitstring
        exeLog.write("++++ resetting bitstring\n")
        print("++++ resetting bitstring")
        for bool in wasUsedList:
            wasUsedList[bool] = False
        trueAmount = 0

    j = 0
    while j != lineNo:
        line = fp.readline()
        j = j + 1
    print("got through for")
    sayingUse = fp.readline() # set sayingUse to that line
    #sayingUse = sayingUse.decode('utf-8')
    try:
        exeLog.write(useTrend + "\n")
    except:
        exeLog.write("###ERROR: trend not able to be recorded for unknown reason\n")

    sayingUse = sayingUse.replace('+', useTrend)
    sayingUse = sayingUse.replace('$', useTrend + "'s")
    useTrendPlural = useTrend + "s"
    #print(useTrendPlural)
    if isPlural:
        #print("it's plural!")
        sayingUse = sayingUse.replace('@', "are")     #set of things to replace if the word is plural
        sayingUse = sayingUse.replace('[', "")
        sayingUse = sayingUse.replace(']', "have")
        sayingUse = sayingUse.replace('=', "do")
        sayingUse = sayingUse.replace('#', useTrend)
        sayingUse = sayingUse.replace('^', "don't")
        sayingUse = sayingUse.replace('~', "")
        sayingUse = sayingUse.replace('$', "do")
    else:
        sayingUse = sayingUse.replace('@', "is")      #set of things to replace if the word is singular
        sayingUse = sayingUse.replace('[', "a")
        sayingUse = sayingUse.replace(']', "has")
        sayingUse = sayingUse.replace('=', "does")
        sayingUse = sayingUse.replace('#', useTrendPlural)
        sayingUse = sayingUse.replace('^', "doesn't")
        sayingUse = sayingUse.replace('~', "s")
        sayingUse = sayingUse.replace('$', "does")
    #print(sayingUse)
    fp.close()

    message = sayingUse
    api.update_status(message)
    print(message)
    try:
        exeLog.write(message)
    except:
        exeLog.write("###ERROR: message not able to be recorded for unknown reason\n")
    print("updated status")
    exeLog.write("updated status"  + "\n\n")


    print('gotta print now')

    randSec = random.randint(1800, 7200)
    print("now waiting " + str(randSec/60) + " minutes")
    exeLog.write("now waiting " + str(randSec/60) + " minutes\n")
    time.sleep(randSec)



exeLog.close()