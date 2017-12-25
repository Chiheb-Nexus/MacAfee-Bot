from django.shortcuts import render
import twitter

CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET_KEY'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_SECRET= 'YOUR_ACCESS_SECRET_TOKEN'

MACAFEE_ACCOUNT = 'officialmcafee'

def get_tweets(request):
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_SECRET)
    tweets_all = api.GetUserTimeline(screen_name=MACAFEE_ACCOUNT, exclude_replies=True, include_rts=False)
    #tweets_all = api.GetStatus(1)
    print(tweets_all)
    return render(request, 'get_tweets.html', {'tweets_all': tweets_all})
