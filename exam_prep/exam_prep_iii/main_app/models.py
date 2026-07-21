from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from main_app.managers import (
    AuthorManager,
)

# Create your models here.

class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        help_text='Represents the full name of the author.',
    )
    email = models.EmailField(
        unique=True,
        help_text='Represents the email address of the author.',
    )
    is_banned = models.BooleanField(
        default=False,
        help_text='Indicates whether the author is currently banned.'
    )
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
            ],
        help_text='Represents the year of birth of the author.'
    )
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Represents the URL of the author's website.",
    )
    objects = AuthorManager()

    def __str__(self):
        return self.full_name

class Article(models.Model):

    CATEGORY_CHOICES = (
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education'),
    )

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5),
        ],
        help_text='Represents the title of the article.',
    )
    content = models.TextField(
        validators=[
            MinLengthValidator(10),
        ],
        help_text="Provides the content of the article.",
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        max_length=10,
        default='Technology',
        help_text='Represents the category of the article.'
    )
    authors = models.ManyToManyField(
        'Author',
        related_name='articles',
    )
    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.title

class Review(models.Model):
    content = models.TextField(
        validators=[
            MinLengthValidator(10),
        ],
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ],
    )
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.content[:50]