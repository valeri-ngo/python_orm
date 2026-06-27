from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class StudentIDField(models.PositiveIntegerField):
    
    def to_python(self, value):
        if value is None:
            return value
        
        try:
            value = int(float(value))
        except (TypeError, ValueError):
            raise ValueError('Invalid input for student ID')
        
        return value
    
    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        if value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')
        
class Student(models.Model):
    name = models.CharField(
        max_length=100
    )
    student_id = StudentIDField()