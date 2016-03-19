from django.db import models

from django.conf import settings

from django.utils import timezone

from django.contrib.auth.models import User

from django.db.models.signals import post_save

import datetime

from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True, related_name='profile')
	phone_number = models.CharField(max_length=10, default='no phone', null=True)
	avatar = models.ImageField(upload_to='avatar/', default='avatar')
	birthday = models.DateField(null=True)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(default=timezone.now)

class Cadavre(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=30, default='Titre')
	sentance_max = models.IntegerField(default=6, validators=[MinValueValidator(3), MaxValueValidator(1000000)])
	sentance_len = models.IntegerField(default=0)
	like = models.IntegerField(default=0)

	completed = models.BooleanField(default=False)

	def __unicode__(self):
		
		return u'%s' % (self.title)

class Sentance(models.Model):

	user = models.ForeignKey(User)
	cadavre = models.ForeignKey(Cadavre)
	sentance = models.CharField(max_length=60, default="le bourgeon dans la plaine")

	def __unicode__(self):
		
		return u'%s' % (self.sentance)
