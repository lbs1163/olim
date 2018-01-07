# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hair(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/hair/', default='images/hair/default.png')

class Eye(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/eye/', default='images/eye/default.png')

class Clothes(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/clothes/', default='images/clothes/default.png')

class Character(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	hair = models.ForeignKey(Hair)
	eye = models.ForeignKey(Eye)
	clothes = models.ForeignKey(Clothes)
