from models import User, Feedback, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

u1 = User.register(username='chickenlover',
          password='ilovechicken',
          email='chicken@bock.com',
          first_name='Joe',
          last_name='Chicken')

u2 = User.register(username='mark1',
          password='iammark',
          email='mark@site.com',
          first_name='Mark',
          last_name='Klar')

db.session.add_all([u1, u2])
db.session.commit()

f1 = Feedback(title='Check out my username',
              content='Title says it all',
              username='chickenlover')

f2 = Feedback(title='But I dont like...',
              content='Ducks.  I know, surprising.',
              username='chickenlover')

f3 = Feedback(title='Marklar Marklar',
              content='Marklar marklar marklar',
              username='mark1')

f4 = Feedback(title='My name is Mark',
              content='Mark Klar',
              username='mark1')

f5 = Feedback(title='I enjoy South Park',
              content='It is very funny',
              username='mark1')

db.session.add_all([f1,f2,f3,f4,f5])
db.session.commit()