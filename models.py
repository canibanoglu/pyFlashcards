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
    """
    This class represents one flashcard. All Flashcard objects must have a
    question and an answer.
    """
    question = Column(Unicode(length=200))
    answer = Column(Unicode(length=200))
    date_added = Column(DateTime)
    needs_review = Column(Boolean)
    review_count = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')

    def __init__(self, question, answer, category, date_added=None,
                 needs_review=False,
                 review_count=0,
                 mistakes=0,
                 corrects=0):
        self.question = question
        self.answer = answer
        self.date_added = datetime.now() if not date_added else date_added
        self.needs_review = needs_review
        self.review_count = review_count
        self.mistakes = mistakes
        self.corrects = corrects
        self.category = category

class Session(Base, StatsMixin):
    """
    This class represents one training session with the application.
    They are simply a collection of Flashcard objects with an associated date
    which represents the date of the training session.
    """

    date = Column(DateTime)
    cards = relationship("Flashcard",
                secondary=association_table,
                backref="sessions")

    def __init__(self):
        self.date = datetime.now()
        self.mistakes = 0
        self.corrects = 0

    def __iter__(self):
        for card in self.cards:
            yield card

    def addCards(self, cards):
        """
        Adds all the cards passed to this method to this Session object.
        The cards parameter is a list containing Flashcard objects.
        """
        self.cards.extend(cards)

class Category(Base):
    """
    Represents a category that a card can belong to.
    """

    name = Column(Unicode(length=80))

    def __init__(self, name):
        self.name = name

