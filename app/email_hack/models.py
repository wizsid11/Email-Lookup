from __future__ import unicode_literals

from django.db import models
class Emailfinder(models.Model):
	name = models.CharField(max_length=120)
	domain = models.CharField(max_length=120)
	secret = models.CharField(max_length=32)
	verified_emails = models.EmailField()

