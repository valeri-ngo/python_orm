from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_str(value):
    for char in value:
        if not char.isalpha() and char != ' ':
            raise ValidationError('Name can only contain letters and spaces')
    
def validate_age(value):
    if value < 18:
        raise ValidationError('Age must be greater than or equal to 18')
    
def validate_phone_number(value):
    if not value.startswith('+359'):
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")
    
    if not value[4:].isdigit():
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")
    
    if len(value) != 13:
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")

class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validate_str
            ]
    )
    age = models.PositiveIntegerField(
        validators=[
            validate_age
            ]
    )
    email = models.EmailField(
        error_messages={
            "invalid": 'Enter a valid email address'}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[validate_phone_number]
    )
    website_url = models.URLField(
        error_messages={
            'invalid': 'Enter a valid URL'
            }
    )