import pytest
import unittest
import json

from models import *
from flashcards_db import FlashcardsDB

with open('test_data.json') as f:
    data = json.load(f)

# Set up the objects to be used with the test data
# It is important to create the Category objects first, so that we can go on to
# create the Flashcard objects.

objects = {
           'categories': {},
           'flashcards': {},
          }

for category in data['categories']:
    objects['categories'][category] = Category(category)

# We are now ready to create the Flashcard objects using the Category objects
for card in data['cards']:
    flashcard = Flashcard(question=card['question'],
                          answer=card['answer'],
                          category=objects['categories'][card['category']])
    objects['flashcards'][card['question']] = flashcard


def clean_db(func):
    def wrapper(self, *args, **kwargs):
        Base.metadata.drop_all(bind=self.db.engine)
        Base.metadata.create_all(bind=self.db.engine)
        func(self, *args, **kwargs)
        print('asldfjalsdjflkasjdfasjkdfjla\n\n\n')
    return wrapper

class FlashcardsDBTest(unittest.TestCase):
    db = FlashcardsDB(debug=True)

    def __init__(self, *args, **kwargs):
        super(FlashcardsDBTest, self).__init__(*args, **kwargs)
        for category in objects['categories'].values():
            self.db.db_session.add(category)
        self.db.db_session.commit()

    def test_add_category(self):
        new_category = Category('French')
        self.db.add_category(new_category)
        self.db.db_session.commit()

        assert new_category in self.db.get_categories()

    def test_add_existing_category(self):
        # Test if clean_db will add a category that is already in the database
        # The self.db will return True if a new object is added, False if not.
        # We expect to get a False.

        existing_category = Category(data['categories'][0])
        check = self.db.add_category(existing_category)
        assert not check

    def test_add_card_without_explicit_category_adds(self):
        new_cat = Category('English')
        new_card = Flashcard(question='Hello', answer='Bonjour', category=new_cat)
        self.db.add_card(new_card)
        self.db.db_session.commit()

        # Check if the categories have also been added to the self.db
        db_categories = self.db.get_categories()
        assert new_cat in db_categories

        db_cards = self.db.get_cards()
        assert new_card in db_cards

    def test_add_card_with_explicit_category_add(self):
        cat = Category("Star Wars")
        self.db.add_category(cat)
        self.db.db_session.commit()

        card = Flashcard(question='The Emperor', answer='Rocks', category=cat)
        self.db.add_card(card)

        db_cards = self.db.get_cards()
        db_categories = self.db.get_categories()
        assert cat in db_categories
        assert card in db_cards

    def test_add_existing_card(self):
        existing_card = self.db.get_cards()[0]
        new_card = Flashcard(question=existing_card.question,
                             answer=existing_card.answer,
                             category=existing_card.category)
        check = self.db.add_card(new_card)
        assert not check
        assert existing_card.needs_review == True

if __name__ == "__main__":
    unittest.main()
