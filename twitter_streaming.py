from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import model

TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

class StdOutListener(StreamListener):

    def on_data(self, data):
        # print data
        data_dict = json.loads(data)
        # print data_dict.keys()
        # if data_dict['lang'] == 'en':
        if data_dict.get('coordinates'):
            new_tweet = model.Tweet()
            new_tweet.text = data_dict['text']
            new_tweet.latitude = float(data_dict['coordinates']['coordinates'][0])
            new_tweet.longitude = float(data_dict['coordinates']['coordinates'][1])

            model.session.add(new_tweet)
            model.session.commit()

            print data_dict['coordinates']['coordinates']
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)

    stream.filter(track=['cat', 'kitten', 'kitty'])
