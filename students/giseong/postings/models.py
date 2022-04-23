from django.db import models

class Posting(models.Model):
    board      = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

class Image(models.Model):
    image_url = models.URLField(max_length=500)
    posting   = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class Comment(models.Model):
    comment    = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posting    = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'