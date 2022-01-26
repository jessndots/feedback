"""Seed file to make sample data for pets db.""" 

from models import User, db, Feedback
from app import app 


# Create all tables 
db.drop_all()
db.create_all() 


# If table isn't empty, empty it
User.query.delete()


# Add users
katy =   User.register('Katy', 'Wright', 'ladyharmony@gmail.com', 'ladyharmony', 'katywright')
catherine = User.register('Catherine', 'Lin', 'catherinelin@gmail.com', 'clin', 'catherinelin')
bailie =  User.register('Bailie', 'Bechtel', 'bailiebechtel@gmail.com', 'bbechtel', 'bailiebechtel')



# Add new objects to session, so they'll persist
db.session.add(katy)
db.session.add(catherine)
db.session.add(bailie) 
				


# Commit--otherwise, this never gets saved!
db.session.commit()



# Add feedback
f_katy = Feedback(title="Title", content="content content content content content content content content", username='ladyharmony')

db.session.add(f_katy)
db.session.commit()