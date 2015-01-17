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

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///twittermap")
engine = create_engine(DATABASE_URL, echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Date)
    time = Column(Time)


    def add_tags(self, text):
        tags_dict = {'packers': ['packers', 'green bay', 'wisconsin', 'the pack', 'cheeseheads', 'rodgers', 'mccarthy', 'crosby'],
                     'colts': ['colts', 'indianapolis', 'indy', 'luck', 'pagano', 'vinatieri'],
                     'patriots': ['patriots', 'pats', 'new england', 'brady', 'gronk', 'belichick', 'gustowski'],
                     'seahawks': ['seahawks', 'hawks', 'seattle', 'wilson', 'sherman', 'carroll', 'hauschka']}

        for team, tags in tags_dict.iteritems():
            for tag in tags:
                if tag in text.lower():
                    self.new_tag(team)
                    break


    def new_tag(self, tag):
        new_tag = Tag()
        new_tag.tweet_id = self.id
        new_tag.tag = tag

        session.add(new_tag)
        session.commit()


    def add_date(self, twitter_date):
        date = datetime.strptime(twitter_date, '%a %b %d %H:%M:%S +0000 %Y')
        self.date = date.strftime('%B %d, %Y')
        self.time = date.strftime('%H:%M:%S')


class Tag(db.Model):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tag = Column(String(30))

    tweet = relationship("Tweet", backref=backref("tags", order_by=id))



def new_tweet(data):
    new_tweet = Tweet()
    new_tweet.text = data['text']
    new_tweet.latitude = float(data['coordinates']['coordinates'][1])
    new_tweet.longitude = float(data['coordinates']['coordinates'][0])
    
    new_tweet.add_date(data['created_at'])

    session.add(new_tweet)
    session.commit()

    new_tweet.add_tags(data['text'])



def connect():
    """ Used for connecting and creating the database. """

    global ENGINE
    global Session

    ENGINE = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=ENGINE)
    return Session()


def main():
    # rand_tweet = random.randrange(1, model.session.query(model.Question).count())
    pass


if __name__ == "__main__":
    main()