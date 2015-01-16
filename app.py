import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
import model
import random
import json

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "abcdefg")

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///carolineorsi/twittermap")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def index():
    """ This is the 'cover' page of the site """

    return render_template("index.html")


@app.route("/get-tweet")
def get_tweet():
    rand_key = random.randrange(1, model.session.query(model.Tweet).count())
    tweet = model.session.query(model.Tweet)[rand_key]

    tweet_to_return = {}
    tweet_to_return['text'] = tweet.text
    tweet_to_return['latitude'] = tweet.latitude
    tweet_to_return['longitude'] = tweet.longitude

    return jsonify(tweet_to_return)


if __name__ == "__main__":
    model.db.init_app(app)

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)