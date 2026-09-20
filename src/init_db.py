'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):Samuel Simon, Lucas Roque, Sagun Shrestha
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course

# TODO
courses = [
   ('CS', '3250', 'Software Development Methods and Tools', 4),
   ('NAP', '1010', 'Introduction to Napping', 3),
   ('DOG', '2200', 'Advanced Belly Rubs', 4),
   ('GIT', '4040', 'Merge Conflicts and Crying', 3),
   ('MEME', '3000', 'History of Bop It Commercials', 2),
   ('PROC', '1999', 'Procrastination Theory', 1) #which we can finish later, maybe
]

with app.app_context():
    for prefix, number, name, credits in courses:
        course = Course(prefix=prefix, number=number, name=name, credits=credits)
        db.session.add(course)
    db.session.commit()
    print(f'Loaded {len(courses)} courses.')
