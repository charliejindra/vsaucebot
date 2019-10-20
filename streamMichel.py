#!/usr/bin/python3.3
# last edit 7/23/2019
# Charlie Jindra
import tweepy as tp
from twitter import *     # twitter api
import time
import datetime          # datetime class
import random            # rng
import pytz              # python timezones
import smtplib, ssl
from METHODS_Stream import *
import APIKeys
import json

rootTime = time.time() # time execution starts

#twitter API credentials
ckey = APIKeys.ckey
csecret = APIKeys.csecret
atoken = APIKeys.atoken
asecret = APIKeys.asecret

#start michelChecker tweepy instance
auth = tp.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
michelChecker = tp.API(auth)
lastStatusText = ""
lastStatusTime = time.time()
print('michelChecker 1.0 booted')

#incrementing the log number
runNo = open("streamLogs/runNo.txt", 'r') # open runNo in r to read number its on
currentNo = int(runNo.read())
runNo.close()
runNo = open("streamLogs/runNo.txt", 'w') # open runNo in w to write the incremented v on it
currentNo = currentNo + 1
runNo.write(str(currentNo))    # now writing the new number to runNo
runNo.close()

# makin a new log each time yea boi
exeLog = open("streamLogs/streamLog"+str(currentNo)+".txt", 'w+') # create new log for this edition yaye, w+ makes new file
print("started log" + str(currentNo))

TCPTime = time.time()
#function to reply or like a tweet given to it
while True:

    stream = TwitterStream(auth=OAuth(
    atoken, asecret, ckey, csecret), timeout=None)

    iterator = stream.statuses.filter(follow="395477244", track="vsauce,@vsaucebot,@tweetsauce") #1863401324 me 395477244 tweetsauce

    TCPDuration = time.time() - TCPTime #get time since last tcp connection

    TCPTime = time.time() # set tcpTime for next time

    print('+//////////////////////////////+')
    print('initialized new TCP connection.')
    print('time since last init: {}'.format(prettifyTime(TCPDuration)))
    print('time since start of execution: {}'.format(prettifyTime(time.time() - rootTime)))
    print('+//////////////////////////////+')

    lastMessageTime = time.time()
    for status in iterator:
        try:
            screen_name = status["user"]["screen_name"]
            content = status["text"]
            # cant be michelbots tweet and cant be favorited by me already or be another bot bc that got annoying
            if (not screen_name == "vsaucebot") and (status["favorited"] == False) and (not "bot" in screen_name) and (checkIfVsauceInText(status) or screen_name == "tweetsauce"):
                print("+--------------------------+")
                print(content)
                print("+--------------------------+")
                encodedString = content
                try:
                    encodedString.decode('utf8') #encode that shit if it needs it
                except:
                    time.sleep(0)
                randoReply = random.randint(0, 100)                # random chance to reply to a rando.
                if (screen_name == "tweetsauce") or (randoReply < 6): # reply to vsauce acct branch, TESTACC79527338 for tests
                    if (content[0] == 'R' and content[1] == 'T'):  # if its a RT
                        print("3. Ended because retweeted status\n\n")
                    else:
                        print("1. Replying to a tweet!")
                        listOfWords = encodedString.split(' ')
                        wordChoice = ""
                        topWordScore = 0
                        topWordJoin = 0
                        for i in range(len(listOfWords)):
                            wordIsJoin = 0
                            wordScore = 0
                            #now for stripping off punctuation bc thats just lame
                            listOfWords[i] = listOfWords[i].strip('.')
                            listOfWords[i] = listOfWords[i].strip(',')
                            listOfWords[i] = listOfWords[i].strip('!')
                            listOfWords[i] = listOfWords[i].strip('(')
                            listOfWords[i] = listOfWords[i].strip(')')
                            wordScore = wordScore + len(listOfWords[i])
                            if listOfWords[i][0].isupper():     #if its a capitalized word
                                wordScore = wordScore + 1.5
                            if i != len(listOfWords) - 1:
                                if listOfWords[i+1][0].isupper() and not listOfWords[i+1].isupper():   #if the word after is a capitalized one, and not all caps
                                    wordScore = wordScore + 2.5
                                    wordIsJoin = wordIsJoin + 1 #add the word to the list
                            if (wordScore > topWordScore) and (not "http" in listOfWords[i]) and (not "@" in listOfWords[i]) and (not listOfWords[i] == "vsauce") and (not listOfWords[i] == "Vsauce"):   # figuring out if this word beats the top word.
                                wordChoice = listOfWords[i]
                                topWordScore = wordScore
                                topWordJoin = wordIsJoin    #set topwordjoin value to the one of the word.
                                wordIndex = i
                                #print("   New Word: " + wordChoice)
                                #print("   Score:    " + topWordScore)
                        if topWordJoin == 1:                                        # if the word won bc of joiny then go add that other word now!
                            wordChoice = wordChoice + " " + listOfWords[wordIndex+1]
                        print("Word Chosen: " + wordChoice)
                        exeLog.write("Word Chosen: " + wordChoice)
                        tweetBuilder = makeStatus(wordChoice)
                        #print("got past make status")
                        replyToStatus(status, tweetBuilder)
                        print("replied successfully!")
                        print(tweetBuilder) #prints what it would tweet minus the @

                        if (screen_name == "tweetsauce"):       #indicate in the subject youre replying to a vsauce tweet if vsauce tweet
                            subject = "I replied to a Vsauce tweet!!"
                        else:
                            subject = "I replied to a tweet!"
                        msg = screen_name+" tweeted:\n"+content+"\n\nI tweeted:\n@tweetsauce "+tweetBuilder+"\n\nLink to tweet: https://twitter.com/TESTACC79527338/status/" +status["id_str"]  #obv TESTACC79527338 for test, tweetsauce for actual
                        #msg = screen_name+" tweeted:\n\n"+content+"\n\nI would've tweeted:\n\n@tweetsauce "+tweetBuilder

                        #send_email(subject, msg, exeLog)

                        print('! Time since last message: {}'.format(prettifyTime(time.time() - lastMessageTime)))
                        print('! Time since start of execution: {}'.format(prettifyTime(time.time() - rootTime)))
                        lastMessageTime = time.time()
                else:                                             # favorite tweet that mentioned vsauce branch
                    if (content[0] == 'R' and content[1] == 'T'):  # if its a RT
                        print("3. Ended because retweeted status\n\n")
                    else:
                        print("first two letters are: [" + content[0] + content[1] + "]") #checking to see why the RT block isnt working nvm it is
                        print("2. Liking a tweet!")
                        #print(status.favorited)
                        api.create_favorite(status["id"])

                        subject = "I liked a tweet!"
                        msg = screen_name+" tweeted:\n\n"+content

                        #send_email(subject, msg, exeLog)
                        
                        print('! Time since last message: {}'.format(prettifyTime(time.time() - lastMessageTime)))
                        print('! Time since start of execution: {}'.format(prettifyTime(time.time() - rootTime)))
                        lastMessageTime = time.time()



                #api.send_direct_message(screen_name="CharlieJindra", text="brian got prankd")
                #api.send_direct_message(1220165389, "ur a butt lol")

        except:
            print("Didn't work somewhere along the way, went to except\n")
        
        # MICHELCHECKER -- CHECKS WHETHER MICHELBOT IS DOWN
        mostRecentStatuses = michelChecker.user_timeline(screen_name="vsaucebot", count=20)
        statusNum = 0
        mostRecentStatus = mostRecentStatuses[statusNum]
        try:
            while mostRecentStatus.in_reply_to_status_id != None: #first gets to a status that's not a reply
                statusNum = statusNum + 1
                mostRecentStatus = mostRecentStatuses[statusNum]
        except: # if every tweet was a reply... something's terribly wrong.
            print('michelbot status - last 20 tweets brought up nothing. michel is big down')
            subject = "Michelbot is big down"
            msg = "I looked through michel's last 20 tweets and nothing was a non-reply. Michelbot is big dead."

            send_email(subject, msg, exeLog)
        timeSinceLastMichel = time.time() - lastStatusTime
        if mostRecentStatus.text == lastStatusText: #if the status is still the same as last time, check to see how long since that was posted
            if timeSinceLastMichel > 7200: #if the time since it was posted is more than 2 hours send an email
                print('michelbot status - he may be down. check up on him')
                subject = "Michelbot might be down"
                msg = "Michelbot's last tweet was tweeted {} ago. This warning was sent because michelbot should be tweeting more frequently than this.".format(prettifyTime(timeSinceLastMichel))

                send_email(subject, msg, exeLog)

        else: # if the status is different now update it and reset the waiting clock to 0 sec
            print('michelbot status - he tweeted!')
            lastStatusText = mostRecentStatus.text
            lastStatusTime = time.time()

    print("<TCP Connection Lost!>")
    print("<Waiting 5 minutes to avoid API GET limit.>")
    countdown = 5
    while countdown != 0:
        print("<{} Minutes Remaining>".format(countdown))
        time.sleep(60)
        countdown = countdown - 1

        
        
        
        
        

# #login to twitter account as:
# auth = tp.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
# api = tp.API(auth)
# print('running!')



#creating stream for replies and likes
#overriding mystreamlistener to add logic to on_status
# class MyStreamListener(tp.StreamListener):
#     def on_status(self, status):
#         reactToTweet(status) #send status into reactToTweet function

#     def on_timeout(self):
#         print('timed out')
#         exeLog.write("###########################TIMEOUT##############################")

#actually making stream
# myStreamListener = MyStreamListener()
# myStream = tp.Stream(auth = api.auth, listener=myStreamListener)

#listOfTweets = api.user_timeline(screen_name="tweetsauce", count=20)
#for tweet in listOfTweets:
#    reactToTweet(tweet)

#stream filter (thing that keeps runnin forever)
#myStream.filter(follow=["395477244"], track=['@vsaucebot', 'vsauce', 'michael stevens']) #1114526834962632705 testacct 395477244 tweetsauce