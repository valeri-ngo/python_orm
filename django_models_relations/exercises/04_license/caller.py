import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Driver, DrivingLicense
from datetime import timedelta
from datetime import date

# Create queries within functions
def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')

    result = []

    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)

        result.append(f"License with number: {license.license_number} expires on {expiration_date}!")
    
    return '\n'.join(result)

def get_drivers_with_expired_licenses(due_date: date):
    return Driver.objects.filter(license__issue_date__lte=due_date - timedelta(days=365)
    )

# Print