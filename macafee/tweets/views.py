from django.shortcuts import render
from .user_settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, TWITTER_USER
import twitter
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
#import cv2

class ParseLinks:

    def parse_html(self, data):
        soup = bs(data, 'html.parser', from_encoding="iso-8859-1")
        div_image = soup.find_all('img')
        try:
            image = div_image
            return image
        except Exception as e:
            return None



    def parse_tweets(self, htmls):
        '''
        example:
        '<blockquote class="twitter-tweet" data-conversation="none">
            <p lang="en" dir="ltr">Good man. But in any case, now is the time to buy any Cryptocurrency whatsoever.
            You can&#39;t possibly lose. Just commit to celebrating Christmas a few days late:)</p>
            &mdash; John McAfee (@officialmcafee)
            <a href="https://twitter.com/officialmcafee/status/944301040777744384?ref_src=twsrc%5Etfw">
            December 22, 2017
            </a>
        </blockquote>\n
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n'
        '''
        for html in htmls:
            soup = bs(html, 'html.parser')
            link = soup.find('a')['href']
            print(link)
            yield link

    def get_images(self, htmls):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'method': 'GET',
            'authority': 'twitter.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        for link in self.parse_tweets(htmls):
            req = Request(link, headers=headers)
            with urlopen(req) as f:
                data = f.read()

            print(data.decode('iso-8859-1'))
            image_link = self.parse_html(data.decode('iso-8859-1'))
            yield image_link



class MacAfeeTweets:
    def __init__(self, user):
        self.user = user
        self.API = twitter.Api(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token_key=ACCESS_TOKEN,
                               access_token_secret=ACCESS_SECRET)

    def get_user_timeline(self):
        return self.API.GetUserTimeline(screen_name=self.user, exclude_replies=True, count=50)

    def get_status_oembed(self, status_id):
        return self.API.GetStatusOembed(status_id=status_id, hide_thread=True)

    def get_images_text(self):
        timeline = (k.id for k in self.get_user_timeline())
        status_oembed = [self.get_status_oembed(k)['html'] for k in timeline]
        images = list(ParseLinks().get_images(status_oembed))

        print(images)
        return status_oembed


def get_tweets(request):
    macafee = MacAfeeTweets(TWITTER_USER)
    tweets_all = macafee.get_user_timeline()
    ids = (k.id for k in tweets_all)
    tweets_oembed_html = [macafee.get_status_oembed(k)['html'] for k in ids]

    return render(request, 'get_tweets.html', {'tweets_all': zip(tweets_all, tweets_oembed_html)})

def get_tweets_images_text(request):
    macafee = MacAfeeTweets(TWITTER_USER)
    status_oembed = macafee.get_images_text()
    #print(status_oembed)

    return render(request, 'get_tweets_text.html', {'tweets_all': status_oembed})
