from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from main_app.managers import (
    PublisherManager,
)

# Create your models here.

class CountryMixin(models.Model):
    country = models.CharField(
        max_length=40,
        default = "TBC",
    )

    class Meta:
        abstract = True

class RatingMixin(models.Model):
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
    )

    class Meta:
        abstract = True

class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True

class Publisher(CountryMixin, RatingMixin, models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3),],
    )
    established_date = models.DateField(
        default='1800-01-01',
    )
    objects = PublisherManager()

    def __str__(self):
        return self.name

class Author(CountryMixin, UpdatedAtMixin, models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3),],
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name

class Book(RatingMixin, UpdatedAtMixin, models.Model):

    GENRE_CHOICES = (
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Other', 'Other'),
    )

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2),],
    )
    publication_date = models.DateField()
    summary = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.CharField(
        max_length=11,
        choices=GENRE_CHOICES,
        default='Other',
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(9999.99),
        ],
        default=0.01
    )
    is_bestseller = models.BooleanField(
        default=False,
    )
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.CASCADE,
        related_name='books',
    )
    main_author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='books',
    )
    co_authors = models.ManyToManyField(
        'Author',
        related_name='co_authors_books',
    )

    def __str__(self):
        return self.title