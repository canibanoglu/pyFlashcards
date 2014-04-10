from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import models

engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)

flashcard1 = models.Flashcard(question='firstquestion', answer='firstanswer')
flashcard2 = models.Flashcard(question='secondquestion', answer='secondanswer')
flashcard3 = models.Flashcard(question='thirdquestion', answer='thirdanswer')
flashcard4 = models.Flashcard(question='fourthquestion', answer='fourthanswer')
flashcard5 = models.Flashcard(question='fifthquestion', answer='fifthanswer')

card_session1 = models.Session()
card_session1.cards.append(flashcard1)
card_session1.cards.append(flashcard2)

card_session2 = models.Session()
card_session2.cards.append(flashcard3)
card_session2.cards.append(flashcard4)
card_session2.cards.append(flashcard5)

print("Created 5 flashcard objects and 2 session objects\n")
print("Creating the required tables\n")

models.Base.metadata.create_all(engine)

print("Adding everything to the database")

db_session = Session()
db_session.add_all([card_session1, card_session2])
db_session.commit()

print("\nChanges have been committed to the database.\n")

retrieved_card = db_session.query(models.Flashcard).filter_by(question='firstquestion').one()
retrieved_session = db_session.query(models.Session).all()[1]

print("Retrieved card's question:", retrieved_card.question)
print("Retrieved card's answer:", retrieved_card.answer)
print("Retrieved card's sessions:", retrieved_card.sessions)
print("Retrieved card's mistakes:", retrieved_card.mistakes)

print("Retrieved session's cards:", retrieved_session.cards)
