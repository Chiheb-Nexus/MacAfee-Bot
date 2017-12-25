from django.conf.urls import include, url
from .views import get_tweets

urlpatterns = [
    url('^get-tweets/', get_tweets, name='get_tweets')
]
