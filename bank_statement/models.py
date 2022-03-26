from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    telephone = models.IntegerField()
    bank = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=20, default='undefined')


class UserStatement(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='statement'
    )
    statement_date = models.DateField()
    add_date = models.DateField(auto_now_add=True)
    sum_total = models.FloatField()


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    add_date = models.DateField(auto_now_add=True)
