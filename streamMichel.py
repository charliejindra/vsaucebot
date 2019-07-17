#!/usr/bin/python3.3
# last edit 6/7/2019
# Charlie Jindra
import tweepy as tp      # twitter api
from twitter import *
import time
import datetime          # datetime class
import random            # rng
import pytz              # python timezones
import smtplib, ssl
from METHODS_Stream import *
import APIKeys

#function to reply or like a tweet given to it
def reactToTweet(status):
    try:
        if (not status.user.screen_name == "vsaucebot") and (status.favorited == False) and (not "bot" in status.user.screen_name): # cant be michelbots tweet and cant be favorited by me already or be another bot bc that got annoying
            print("+--------------------------+")
            print(status.text)
            print("+--------------------------+")
            encodedString = status.text
            try:
                encodedString.decode('utf8') #encode that shit if it needs it
            except:
                time.sleep(0)
            randoReply = random.randint(0, 100)                # random chance to reply to a rando.
            if (status.user.screen_name == "tweetsauce") or (randoReply < 6): # reply to vsauce acct branch, TESTACC79527338 for tests
                if (status.text[0] == 'R' and status.text[1] == 'T'):  # if its a RT
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
                    api.update_status("@"+ status.user.screen_name+" " + tweetBuilder, status.id) #run the big ol function at the top # reply to vsauce acct branch, TESTACC79527338 for tests
                    print("replied successfully!")
                    print(tweetBuilder) #prints what it would tweet minus the @

                    if (status.user.screen_name == "tweetsauce"):       #indicate in the subject youre replying to a vsauce tweet if vsauce tweet
                        subject = "I replied to a Vsauce tweet!!"
                    else:
                        subject = "I replied to a tweet!"
                    msg = status.user.screen_name+" tweeted:\n"+status.text+"\n\nI tweeted:\n@tweetsauce "+tweetBuilder+"\n\nLink to tweet: https://twitter.com/TESTACC79527338/status/" +status.id_str  #obv TESTACC79527338 for test, tweetsauce for actual
                    #msg = status.user.screen_name+" tweeted:\n\n"+status.text+"\n\nI would've tweeted:\n\n@tweetsauce "+tweetBuilder

                    send_email(subject, msg, exeLog)


            else:                                             # favorite tweet that mentioned vsauce branch
                if (status.text[0] == 'R' and status.text[1] == 'T'):  # if its a RT
                    print("3. Ended because retweeted status\n\n")
                else:
                    print("first two letters are: [" + status.text[0] + status.text[1] + "]") #checking to see why the RT block isnt working nvm it is
                    print("2. Liking a tweet!")
                    #print(status.favorited)
                    api.create_favorite(status.id)

                    subject = "I liked a tweet!"
                    msg = status.user.screen_name+" tweeted:\n\n"+status.text

                    send_email(subject, msg, exeLog)



                #api.send_direct_message(screen_name="CharlieJindra", text="brian got prankd")
                #api.send_direct_message(1220165389, "ur a butt lol")

    except:
        print("Didn't work somewhere along the way, went to except\n")

#twitter API credentials
consumer_key = APIKeys.ckey
consumer_secret = APIKeys.csecret
access_token = APIKeys.atoken
access_secret = APIKeys.asecret

#login to twitter account as:
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)
print('running!')

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

#creating stream for replies and likes
#overriding mystreamlistener to add logic to on_status
class MyStreamListener(tp.StreamListener):
    def on_status(self, status):
        reactToTweet(status) #send status into reactToTweet function

    def on_timeout(self):
        print('timed out')
        exeLog.write("###########################TIMEOUT##############################")

    # def on_exception(self, exception):
    #     print(exception)
    #     exeLog.write("###########################exception##############################")
    #     exeLog.write("ran into exception") # right now switched from writing exception bc didnt work
    #     return

#actually making stream
myStreamListener = MyStreamListener()
myStream = tp.Stream(auth = api.auth, listener=myStreamListener)

#listOfTweets = api.user_timeline(screen_name="tweetsauce", count=20)
#for tweet in listOfTweets:
#    reactToTweet(tweet)

#stream filter (thing that keeps runnin forever)
myStream.filter(follow=["395477244"], track=['@vsaucebot', 'vsauce', 'michael stevens']) #1114526834962632705 testacct 395477244 tweetsauce