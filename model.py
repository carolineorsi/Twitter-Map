from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Float, and_, or_
from sqlalchemy.orm import sessionmaker, relationship, backref
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from sqlalchemy import ForeignKey
from app import app
import os

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