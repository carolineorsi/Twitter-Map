from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Float, String, Date, Time, and_, or_
from sqlalchemy.orm import sessionmaker, relationship, backref
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from sqlalchemy import ForeignKey
from app import app
from datetime import datetime
import os
import re

db = SQLAlchemy(app)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///superbowl")
engine = create_engine(DATABASE_URL, echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    tweet = Column(String(256))
    username = Column(String(64))
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Date)
    time = Column(Time)


    # def add_tags(self, text):
    #     tags_dict = {'packers': ['packers', 'green bay', 'wisconsin', 'the pack', 'cheeseheads', 'rodgers', 'mccarthy', 'crosby'],
    #                  'colts': ['colts', 'indianapolis', 'indy', 'luck', 'pagano', 'vinatieri'],
    #                  'patriots': ['patriots', 'pats', 'new england', 'brady', 'gronk', 'belichick', 'gustowski'],
    #                  'seahawks': ['seahawks', 'hawks', 'seattle', 'wilson', 'sherman', 'carroll', 'hauschka']}

    #     for team, tags in tags_dict.iteritems():
    #         for tag in tags:
    #             if tag in text.lower():
    #                 self.new_tag(team)
    #                 break


    # def new_tag(self, tag):
    #     new_tag = Tag()
    #     new_tag.tweet_id = self.id
    #     new_tag.tag = tag

    #     session.add(new_tag)
    #     session.commit()

    def add_media(self, media):
        new_media = Media()
        new_media.tweet_id = self.id
        new_media.media_type = media['type']
        new_media.url = media['media_url']
        new_media.start_index = media['indices'][0]
        new_media.end_index = media['indices'][1]

        session.add(new_media)
        session.commit()


    def add_hashtag(self, hashtag):
        new_hashtag = Hashtag()
        new_hashtag.tweet_id = self.id
        new_hashtag.hashtag = hashtag['text']
        new_hashtag.start_index = hashtag['indices'][0]
        new_hashtag.end_index = hashtag['indices'][1]

        session.add(new_hashtag)
        session.commit()


    def add_date(self, twitter_date):
        date = datetime.strptime(twitter_date, '%a %b %d %H:%M:%S +0000 %Y')
        self.date = date.strftime('%B %d, %Y')
        self.time = date.strftime('%H:%M:%S')


# class Tag(db.Model):
#     __tablename__ = "tag"

#     id = Column(Integer, primary_key=True)
#     tweet_id = Column(Integer, ForeignKey('tweet.id'))
#     tag = Column(String(30))

#     tweet = relationship("Tweet", backref=backref("tags", order_by=id))


class Media(db.Model):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    media_type = Column(String(64))
    url = Column(String(256))
    start_index = Column(Integer)
    end_index = Column(Integer)


    tweet = relationship("Tweet", backref=backref("media", order_by=id))


class Hashtag(db.Model):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    hashtag = Column(String(64))
    start_index = Column(Integer)
    end_index = Column(Integer)

    tweet = relationship("Tweet", backref=backref("hashtags", order_by=id))


def new_tweet(data):
    new_tweet = Tweet()
    new_tweet.tweet = data['text']
    new_tweet.latitude = float(data['coordinates']['coordinates'][1])
    new_tweet.longitude = float(data['coordinates']['coordinates'][0])
    new_tweet.username = data['user']['screen_name']
    
    new_tweet.add_date(data['created_at'])

    session.add(new_tweet)
    session.commit()

    if 'media' in data['entities']:
        for item in data['entities']['media']:
            print item
            new_tweet.add_media(item)

    if 'hashtags' in data['entities']:
        for hashtag in data['entities']['hashtags']:
            new_tweet.add_hashtag(hashtag)



    # new_tweet.add_tags(data['text'])
    pass


def connect():
    """ Used for connecting and creating the database. """

    global ENGINE
    global Session

    ENGINE = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=ENGINE)
    return Session()


def main():
    pass


if __name__ == "__main__":
    main()