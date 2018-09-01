from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first = models.TextField()
    last = models.TextField()
    department = models.TextField()
    office = models.TextField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
	Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Dataset(models.Model):

class Distribution(models.Model):

class Schema(models.Model):
    data = JSONField()
