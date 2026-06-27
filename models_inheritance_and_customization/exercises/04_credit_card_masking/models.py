from django.db import models

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class MaskedCreditCardField(models.CharField):
    def to_python(self, value):
        
        if value is None:
            return value
        
        if not isinstance(value, str):
            raise ValidationError('The card number must be a string')

        if not value.isdigit():
            raise ValidationError('The card number must contain only digits')
        
        if len(value) != 16:
            raise ValidationError('The card number must be exactly 16 characters long')
        
        return value
        
    def get_prep_value(self, value):

        if value is None:
            return value
        
        if isinstance(value, str) and value.startswith("****"):
            return value
        
        return f'****-****-****-{value[-4:]}'
        
class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100
    )
    card_number = MaskedCreditCardField(
        max_length = 20
    )
