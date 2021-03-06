import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
import model
import random
import json
from datetime import datetime

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "abcdefg")

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///superbowl")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def index():
    """ This is the 'cover' page of the site """

    return render_template("index.html")


@app.route("/get-tweet")
def get_tweet():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    start_time = int(request.args.get('start_time'))
    tweets_to_return = []
    tags = model.session.query(model.Tag).filter(model.or_(model.Tag.tag==team1, model.Tag.tag==team2)).all()
    # tags = model.session.query(model.Tag).filter(model.or_(model.Tag.tag==team1, model.Tag.tag==team2)).limit(1000)

    for tag in tags:
        tweets = model.session.query(model.Tweet).filter_by(id=tag.tweet_id).all()
        for tweet in tweets:
            tweet_to_return = {}
            tweet_to_return['latitude'] = tweet.latitude
            tweet_to_return['longitude'] = tweet.longitude
            tweet_to_return['color'] = pick_color(tag.tag)

            timestamp = datetime.combine(tweet.date, tweet.time)
            epoch_time = int(timestamp.strftime('%s'))

            if epoch_time > start_time and epoch_time < start_time + 18000:
                tweet_to_return['time'] = epoch_time - start_time

                tweets_to_return.append(tweet_to_return)

    response = {'data': tweets_to_return}

    return jsonify(response)


@app.route("/random-tweet")
def random_tweet():
    rand_key = random.randrange(1, model.session.query(model.Tweet).count())
    tweet = model.session.query(model.Tweet)[rand_key]

    tweet_to_return = {}
    tweet_to_return['text'] = tweet.tweet
    tweet_to_return['latitude'] = tweet.latitude
    tweet_to_return['longitude'] = tweet.longitude

    if tweet.media:
        for media in tweet.media:
            tweet_to_return['media'] = media.url
        print media

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