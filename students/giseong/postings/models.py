from django.db import models

class Posting(models.Model):
    board      = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image      = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

class Image(models.Model):
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = 'images'
