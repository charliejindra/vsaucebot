from twitter import *
import time
import datetime

startTime = datetime.time()

username = "vsauce"
stream = TwitterStream(auth=OAuth(
    atoken, asecret, ckey, csecret), timeout=None)

# Now work with Twitter
#twitter.statuses.update(status='Helloworld!')

iterator = stream.statuses.filter(follow="1863401324", track="vsauce,@vsaucebot,@tweetsauce")

for tweet in iterator:
    if (tweet["in_reply_to_screen_name"] == "TerriblyAcurate"):
        print('hahaaaa gotcha!')
        currentTime = datetime.time()
        sinceStart = currentTime - startTime
        print(sinceStart)
    else:
        print('ok you can go')
    #print(tweet)