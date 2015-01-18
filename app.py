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
#     tweets = model.session.query(model.Tweet).all()
#     tweets_to_return = []

#     for tweet in tweets:
#         tweet_to_return = {}
#         tweet_to_return['text'] = tweet.text
#         tweet_to_return['latitude'] = tweet.latitude
#         tweet_to_return['longitude'] = tweet.longitude
#         tweet_to_return['color'] = pick_color(tweet.tag)

#         if tweet.date and tweet.time and tweet.tag:
#             timestamp = datetime.combine(tweet.date, tweet.time)
#             tweet_to_return['time'] = int(timestamp.strftime('%s')) - 1421454200

#             tweets_to_return.append(tweet_to_return)

#     response = {'data': tweets_to_return}

#     return jsonify(response)


@app.route("/get-tweet")
def get_tweet():
    tweets_to_return = []
    # tags = model.session.query(model.Tag).all()
    tags = model.session.query(model.Tag).filter_by(tag='seahawks').all()

    for tag in tags:
        tweets = model.session.query(model.Tweet).filter_by(id=tag.tweet_id).all()
        for tweet in tweets:
            tweet_to_return = {}
            tweet_to_return['text'] = tweet.text
            tweet_to_return['latitude'] = tweet.latitude
            tweet_to_return['longitude'] = tweet.longitude
            tweet_to_return['color'] = pick_color(tag.tag)

            timestamp = datetime.combine(tweet.date, tweet.time)
            epoch_time = int(timestamp.strftime('%s'))

            if epoch_time > 1421634600:
                tweet_to_return['time'] = epoch_time - 1421634600

                tweets_to_return.append(tweet_to_return)

    response = {'data': tweets_to_return}

    return jsonify(response)


@app.route("/random-tweet")
def random_tweet():
    rand_key = random.randrange(1, model.session.query(model.Tweet).count())
    tweet = model.session.query(model.Tweet)[rand_key]

    tweet_to_return = {}
    tweet_to_return['text'] = tweet.text
    tweet_to_return['latitude'] = tweet.latitude
    tweet_to_return['longitude'] = tweet.longitude

    return jsonify(tweet_to_return)


def pick_color(tag):
    #TODO: move this to JavaScript
    color_dict = {'packers': '#7A9F31',
                  'patriots': '#C80815',
                  'seahawks': '#133579',
                  'colts': '#000000'}

    return color_dict[tag]


if __name__ == "__main__":
    model.db.init_app(app)

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)