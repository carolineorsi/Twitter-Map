import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
import model
import random
import json
from datetime import datetime

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "abcdefg")

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///carolineorsi/twittermap")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def index():
    """ This is the 'cover' page of the site """

    return render_template("index.html")


# @app.route("/get-tweet")
# def get_tweet():
#     rand_key = random.randrange(1, model.session.query(model.Tweet).count())
#     tweet = model.session.query(model.Tweet)[rand_key]

#     timestamp = datetime.combine(tweet.date, tweet.time)
#     print int(timestamp.strftime('%s')) - 1421395200

#     return "success"

@app.route("/get-tweet")
def get_tweet():
    tweets = model.session.query(model.Tweet).all()
    tweets_to_return = []

    for tweet in tweets:
        tweet_to_return = {}
        tweet_to_return['text'] = tweet.text
        tweet_to_return['latitude'] = tweet.latitude
        tweet_to_return['longitude'] = tweet.longitude
        tweet_to_return['color'] = pick_color(tweet.tag)

        if tweet.date and tweet.time:
            timestamp = datetime.combine(tweet.date, tweet.time)
            tweet_to_return['time'] = int(timestamp.strftime('%s')) - 1421454200

            tweets_to_return.append(tweet_to_return)

    response = {'data': tweets_to_return}

    return jsonify(response)

def pick_color(tag):
    if tag == 'packers':
        return '#0f0'
    elif tag == 'patriots':
        return '#f00'
    elif tag == 'seahawks':
        return '#00f'
    elif tag == 'colts':
        return '#666'
    else:
        return '#fff'


if __name__ == "__main__":
    model.db.init_app(app)

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)