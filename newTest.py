from twitter import *
import time
from METHODS_Stream import prettifyTime

print("running!")

startTime = time.time()



username = "vsauce"
stream = TwitterStream(auth=OAuth(
    atoken, asecret, ckey, csecret), timeout=None)

# Now work with Twitter
#twitter.statuses.update(status='Helloworld!')

iterator = stream.statuses.filter(follow="1863401324", track="vsauce,@vsaucebot,@tweetsauce")

for tweet in iterator:
    if "in_reply_to_screen_name" in tweet.keys():
        if tweet["in_reply_to_screen_name"] == "TerriblyAcurate":
            print('hahaaaa gotcha!')
        else:
            print("got in but not reply to TerriblyAcurate")
    else:
        print("wasnt even in the dictionary")
    currentTime = time.time()
    sinceStart = currentTime - startTime
    print("Time since start of stream: " + prettifyTime(sinceStart))