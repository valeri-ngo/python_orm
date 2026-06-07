import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student

# Import your models here

def truncate_students():
    students = Student.objects.all()
    students.delete()

truncate_students()
print(Student.objects.all())
print(f"Number of students: {Student.objects.count()}")