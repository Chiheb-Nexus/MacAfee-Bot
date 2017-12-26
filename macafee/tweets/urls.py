from django.conf.urls import include, url
from .views import get_tweets, get_tweets_images_text

urlpatterns = [
    url(r'^get-tweets/', get_tweets, name='get_tweets'),
    url(r'^get-tweets-text/', get_tweets_images_text, name='get_tweets_text')
]
