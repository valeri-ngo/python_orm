from django.core.exceptions import ValidationError

def digits_validate(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits.')