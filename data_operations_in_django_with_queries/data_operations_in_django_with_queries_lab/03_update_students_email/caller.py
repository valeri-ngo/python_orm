import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student

# Import your models here

def update_students_emails():
    students = Student.objects.all()
    
    for student in students:
        new_email = student.email.replace(
            'university.com',
            'uni-students.com'
        )
        
        student.email = new_email
        student.save()

update_students_emails()
for student in Student.objects.all():
    print(student.email)