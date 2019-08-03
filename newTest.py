from twitter import *
import time
from METHODS_Stream import prettifyTime
import APIKeys

print("running!")

ckey = 'U6o8g2MxTxCjQXb5Ep3UrHDCc'
csecret = 'rsv0VpttVujDpSv3gwwG61b2icfeLY8yI6xN4DZy2Z1GZJXuLU'
atoken = '1114526834962632705-O2db2o6Ng63QCTvqyCqfL9KsH5Hh8y'
asecret = 'yhZ3mJRDeSHuxefwp7hAy7HWqsGGwKNyMAJc55HKICE92'

startTime = time.time()

#twitter API credentials
ckey = ckey
csecret = csecret
atoken = atoken
asecret = asecret

username = "vsauce"
#stream = TwitterStream(auth=OAuth(
 #   atoken, asecret, ckey, csecret), timeout=None, block=True)

# Now work with Twitter
#twitter.statuses.update(status='Helloworld!')

#iterator = stream.statuses.filter(follow="1863401324", track="vsauce,@vsaucebot,@tweetsauce")

twitter_userstream = TwitterStream(auth=OAuth(atoken, asecret, ckey, csecret), domain='userstream.twitter.com')
for msg in twitter_userstream.user():
    if 'direct_message' in msg:
        print(msg['direct_message']['text'])

#while True:
#    for tweet in iterator:
#        if "in_reply_to_screen_name" in tweet.keys():
#            if tweet["in_reply_to_screen_name"] == "TerriblyAcurate":
#                print('hahaaaa gotcha!')
#            else:
#                print("got in but not reply to TerriblyAcurate")
#        else:
#            print("wasnt even in the dictionary")
#        currentTime = time.time()
#        sinceStart = currentTime - startTime
#        print("Time since start of stream: " + prettifyTime(sinceStart))
#        time.sleep(5)