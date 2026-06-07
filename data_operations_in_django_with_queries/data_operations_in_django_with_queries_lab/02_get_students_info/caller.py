import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student

# Import your models here

def get_students_info():
    students = Student.objects.all()
    student_info = []

    for student in students:
        student_info.append(
            f"Student №{student.student_id}: "
            f"{student.first_name} {student.last_name}; "
            f"Email: {student.email}"
        )
    return '\n'.join(student_info)

print(get_students_info())

