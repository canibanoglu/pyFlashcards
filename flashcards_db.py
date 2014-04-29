from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

import os
import models

class FlashcardsDB(object):
    """
    This class handles pretty much all the database usage with the application.
    """
    db_name = 'flashcards.db'

    def __init__(self, db_path=None, debug=False, echo=False):
        pwd = os.path.realpath(__file__)
        db_exists = os.path.exists(os.path.join(pwd, self.db_name))
        if debug:
            self.db_path = ''
        elif not db_exists:
            # We don't have a db yet, so we'll have to create one
            self.db_path = os.path.join(pwd, self.db_name)
        else:
            self.db_path = db_path
        self.engine = create_engine('sqlite://' + self.db_path, echo=echo)
        self.session_factory = sessionmaker(bind=self.engine)
        self.db_session = self.session_factory()

        if debug or not db_exists:
            self._initDB()

    def _initDB(self):
        models.Base.metadata.create_all(self.engine)

    def add_card(self, card):
        """
        Adds the given card to the database. If a card with the question
        is already present in the database, it will be marked for review.
        Returns True if a new card was added, False if we marked an existing
        one for review.
        """
        card_check = self.db_session.query(models.Flashcard).\
                                     filter_by(question=card.question,\
                                     category=card.category).\
                                     first()
        if card_check:
            card_check.needs_review = True
        else:
            self.db_session.add(card)
        return not card_check

    def get_cards(self, category=None):
        # Add some form of limited searching abilities here
        # Like adding a new argument and checking for that
        if category and names:
            return self.db_session.query(models.Flashcard).\
                                   filter_by(category=category).\
                                   all()
        else:
            return self.db_session.query(models.Flashcard).all()

    def add_category(self, category):
        """
        Adds the given category to the database. Works the same as add_card
        method.
        """
        category_check = self.db_session.query(models.Category).\
                                         filter_by(name=category.name).\
                                         first()
        if not category_check:
            self.db_session.add(category)
        return not category_check

    def get_categories(self):
        # Add some form of limited searching abilities here
        # Like adding a new argument and checking for that
        return self.db_session.query(models.Category).all()

    def fuzzy_search(self, class_string, partial_string):
        """
        Performs a fuzzy search (using the LIKE keyword) with the given
        parameters.
        """
        cls = getattr(models, class_string)
        if class_string == "Flashcard":
            field = getattr(cls, "question")
        elif class_string == "Category":
            field = getattr(cls, "name")
        like_string = "%" + partial_string + "%"
        return self.db_session.query(cls).filter(field.like(like_string)).all()


    def create_session(self, category, review=False, limit=50):
        if review:
            cards = self.db_session.query(models.Flashcard).\
                                    filter_by(needs_review = True).\
                                    limit(limit)
        else:
            cards = self.db_session.query(models.Flashcard).\
                                    order_by(func.random()).\
                                    limit(limit)
        f_session = models.Session()
        f_session.addCards(cards)
        return f_session


