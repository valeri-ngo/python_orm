from django.db import models

class Blog(models.Model):
    post = models.TextField()
    author = models.CharField(max_length=35)

