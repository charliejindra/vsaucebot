from twitter import *
import time
from METHODS_Stream import prettifyTime

print("running!")

startTime = time.time()

#twitter API credentials
ckey = APIKeys.ckey
csecret = APIKeys.csecret
atoken = APIKeys.atoken
asecret = APIKeys.asecret

username = "vsauce"
stream = TwitterStream(auth=OAuth(
    atoken, asecret, ckey, csecret), timeout=None, block=True)

# Now work with Twitter
#twitter.statuses.update(status='Helloworld!')

iterator = stream.statuses.filter(follow="1863401324", track="vsauce,@vsaucebot,@tweetsauce")

while True:
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
        time.sleep(5)