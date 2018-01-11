# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, string
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def random_string():
	return unicode(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)))

@python_2_unicode_compatible
class Group(models.Model):
	group_name = models.CharField(max_length=20)

	def __str__(self):
		return self.group_name

@python_2_unicode_compatible
class RegistrationCode(models.Model):
	code = models.CharField(max_length=20, default=random_string)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	group = models.ForeignKey(Group)
	is_used = models.BooleanField(default=False)

	def __str__(self):
		return unicode(self.group) + u" " + self.last_name + self.first_name + " " + self.code

@python_2_unicode_compatible
class Hair(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/hair/', default='images/hair/default.png')

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Eye(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/eye/', default='images/eye/default.png')

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Clothes(models.Model):
	name = models.CharField(max_length=20)
	img = models.ImageField(upload_to='images/clothes/', default='images/clothes/default.png')

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Skill(models.Model):
	name = models.CharField(max_length=20)
	math = models.BooleanField(default=False)
	phys = models.BooleanField(default=False)
	chem = models.BooleanField(default=False)
	life = models.BooleanField(default=False)
	prog = models.BooleanField(default=False)
	health = models.IntegerField(default=10)
	damage = models.IntegerField(default=0)

	def __str__(self):
		return self.name + u"(" + unicode(self.damage) + u")"

@python_2_unicode_compatible
class Character(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	hair = models.ForeignKey(Hair, blank=True, null=True)
	eye = models.ForeignKey(Eye, blank=True, null=True)
	clothes = models.ForeignKey(Clothes, blank=True, null=True)
	group = models.ForeignKey(Group, blank=True, null=True)
	math = models.IntegerField(default=0)
	phys = models.IntegerField(default=0)
	chem = models.IntegerField(default=0)
	life = models.IntegerField(default=0)
	prog = models.IntegerField(default=0)
	skill1 = models.ForeignKey(Skill, blank=True, null=True, related_name='skill1')
	skill2 = models.ForeignKey(Skill, blank=True, null=True, related_name='skill2')
	skill3 = models.ForeignKey(Skill, blank=True, null=True, related_name='skill3')
	skill4 = models.ForeignKey(Skill, blank=True, null=True, related_name='skill4')

	def __str__(self):
		return self.user.last_name + self.user.first_name

@python_2_unicode_compatible
class Monster(models.Model):
	name = models.CharField(max_length=40)
	img = models.ImageField(upload_to='images/monster/', default='images/monster/default.png')
	math_exp = models.IntegerField(default=0)
	phys_exp = models.IntegerField(default=0)
	chem_exp = models.IntegerField(default=0)
	life_exp = models.IntegerField(default=0)
	prog_exp = models.IntegerField(default=0)
	dialog1 = models.CharField(max_length=50, null=True)
	dialog2 = models.CharField(max_length=50, null=True)
	dialog3 = models.CharField(max_length=50, null=True)
	death_dialog = models.CharField(max_length=50, null=True)
	skill = models.ForeignKey(Skill)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Battle(models.Model):
	character = models.OneToOneField(Character, on_delete=models.CASCADE)
	monster = models.ForeignKey(Monster)
	ally_health = models.IntegerField(default=100)
	enemy_health = models.IntegerField(default=0)

	def __str__(self):
		return unicode(self.character)

@python_2_unicode_compatible
class Monsterbook(models.Model):
	group = models.ForeignKey(Group)
	grade = models.CharField(max_length=20, null=True)
	monster = models.ForeignKey(Monster)
	finder = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='finder')
	champion = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='champion')

	def __str__(self):
		return self.monster.name
