from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=20)
    email        = models.EmailField(max_length=128, unique=True)
    password     = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=30)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    posting      = models.ForeignKey('postings.Posting', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'users'
    #
    # def __str__(self):
    #     return self.password