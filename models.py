from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Table, Column, Integer, Unicode, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from mixins import StatsMixin

from datetime import datetime


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

association_table = Table('association', Base.metadata,
        Column('session_id', Integer, ForeignKey('session.id')),
        Column('card_id', Integer, ForeignKey('flashcard.id'))
)

class Flashcard(Base, StatsMixin):
    question = Column(Unicode(length=200))
    answer = Column(Unicode(length=200))
    date_added = Column(DateTime)
    needs_review = Column(Boolean)
    review_count = Column(Integer)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.date_added = datetime.now()
        self.needs_review = False
        self.review_count = 0
        self.mistakes = 0
        self.corrects = 0

class Session(Base, StatsMixin):
    date = Column(DateTime)
    cards = relationship("Flashcard",
                secondary=association_table,
                backref="sessions")

    def __init__(self):
        self.date = datetime.now()
        self.mistakes = 0
        self.corrects = 0
