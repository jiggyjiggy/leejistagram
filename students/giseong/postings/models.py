from django.db import models

class Posting(models.Model):

    image      = models.CharField(max_length=500)
    board      = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postings'