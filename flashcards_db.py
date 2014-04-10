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

    def __init__(self, db_path=None, debug=False):
        pwd = os.path.realpath(__file__)
        db_exists = os.path.exists(os.path.join(pwd, self.db_name))
        if debug:
            self.db_path = ''
        elif not db_exists:
            # We don't have a db yet, so we'll have to create one
            self.db_path = os.path.join(pwd, self.db_name)
        else:
            self.db_path = db_path
        self.engine = create_engine('sqlite://' + self.db_path, echo=True)
        self.session_factory = sessionmaker(bind=self.engine)

        if debug or not db_exists:
            self._initDB()

    def _initDB(self):
        models.Base.metadata.create_all(self.engine)

    @contextmanager
    def _db_session_scope():
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def commit(self, objects):
        """
        Commits all the objects passed to this method to the database.
        objects is a list containing model.Session and model.Flashcard objects.
        """
        with self._db_session_scope() as db_session:
            db_session.add_all(objects)


