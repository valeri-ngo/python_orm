from django.core.exceptions import ValidationError

def is_string_validator(value):
    if not value.isalpha():
        raise ValidationError('Fruit name should contain only letters!')