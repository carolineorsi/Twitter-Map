from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import model
import re

TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

class StdOutListener(StreamListener):

    def on_data(self, data):
        data_dict = json.loads(data)
        if data_dict.get('coordinates'):
            model.new_tweet(data_dict)

            # print data_dict['coordinates']['coordinates']
            # print data_dict['text']
            # print data_dict['entities']
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)

    stream.filter(track=['patriots', 'seahawks', 'nfl', 'superbowl',
                         'super bowl', 'commercial', 'halftime', 'doritos',
                         'budweiser', 'bud', 'godaddy', 'go daddy', 'nascar',
                         'snickers', 't-mobile', 'nissan', 'schwarzenegger', 
                         'terminator', 'mophie', 'wix.com', 'mercedes', 'bmw',
                         'lobby hobby', 'skittles', 'friskies', 'carl\'s jr',
                         'carls jr', 'dove', 'priceline', 'squarespace', 
                         'esurance', 'kia', 'pizza hut', 'lucy bowl', 'toyota',
                         'hawks', 'seattle', 'wilson', 'sherman', 
                         'carroll', 'hauschka', 'pats', 'new england', 'brady',
                         'gronk', 'belichick', 'gustowski', 'deflategate',
                         'puppybowl', 'puppy bowl', 'katy perry', 
                         'missy elliott', 'lenny kravitz'])
