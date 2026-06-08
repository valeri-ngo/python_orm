import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Task

# Create queries within functions

Task.objects.create(
    title = 'Sample Task',
    description = 'This is a sample task description',
    due_date = '2023-10-31',
    is_finished = False
)

def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished = False)

    result = []

    for task in unfinished_tasks:
        result.append(
            f"Task - {task.title} needs to be done until {task.due_date}!")
    
    return '\n'.join(result)

def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()

def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(char) - 3) for char in text)

    Task.objects.filter(title = task_title).update(description = encoded_text)

encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
print(Task.objects.filter(title='Sample Task').first().description)
