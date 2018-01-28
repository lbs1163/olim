# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, string
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

@python_2_unicode_compatible
class Server(models.Model):
	is_open = models.BooleanField(default=True)

	def __str__(self):
		return unicode(self.is_open)

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
class Grade(models.Model):
	name = models.CharField(max_length=5)
	turn = models.IntegerField(default=1)

	def __str__(self):
		return self.name + u": " + unicode(self.turn)

@python_2_unicode_compatible
class Bossgrade(models.Model):
	name = models.CharField(max_length=5)
	turn = models.IntegerField(default=1)

	def __str__(self):
		return self.name + u": " + unicode(self.turn)

@python_2_unicode_compatible
class Skill(models.Model):
	name = models.CharField(max_length=20)
	math = models.BooleanField(default=False)
	phys = models.BooleanField(default=False)
	chem = models.BooleanField(default=False)
	life = models.BooleanField(default=False)
	prog = models.BooleanField(default=False)
	boss = models.BooleanField(default=False)
	improvise = models.BooleanField(default=False)
	health = models.IntegerField(default=10)
	damage = models.IntegerField(default=0)
	limit = models.IntegerField(default=0)

	def type(self):
		if self.boss:
			return "boss"
		elif self.math:
			return "math"
		elif self.phys:
			return "phys"
		elif self.chem:
			return "chem"
		elif self.life:
			return "life"
		elif self.prog:
			return "prog"
		else:
			return "normal"

	def __str__(self):
		if self.boss:
			category = u"[보스]"
		elif self.math:
			category = u"[수학] "
		elif self.phys:
			category = u"[물리] "
		elif self.chem:
			category = u"[화학] "
		elif self.life:
			category = u"[생물] "
		elif self.prog:
			category = u"[프밍] "
		else:
			category = u"[일반] "
		return category + self.name + u"(" + unicode(self.health) + u", " + unicode(self.damage) + u", " + unicode(self.limit) + u")"

@python_2_unicode_compatible
class FailedCombination(models.Model):
	group = models.ForeignKey(Group)
	skill001 = models.ForeignKey(Skill, related_name='skill001')
	skill002 = models.ForeignKey(Skill, related_name='skill002')

	def __str__(self):
		return u"[" + self.group.group_name + u"] " + self.skill001.name + u" + " + self.skill002.name
@python_2_unicode_compatible
class Combination(models.Model):
	skill01 = models.ForeignKey(Skill, related_name='skill01')
	skill02 = models.ForeignKey(Skill, related_name='skill02')
	new_skill = models.ForeignKey(Skill, related_name='new_skill')
	
	def __str__(self):
		return self.new_skill.name + u" = " + self.skill01.name + u" + " + self.skill02.name

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
class Have(models.Model):
	character = models.ForeignKey(Character)
	skill = models.ForeignKey(Skill)
	number = models.IntegerField(default=0)

	def __str__(self):
		return unicode(self.character) + u" has " + unicode(self.number) + u" " + unicode(self.skill)

@python_2_unicode_compatible
class Map(models.Model):
	name = models.CharField(max_length=40)
	is_open = models.BooleanField(default=False)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Monster(models.Model):
	name = models.CharField(max_length=40)
	img = models.ImageField(upload_to='images/monster/', default='images/monster/default.png')
	math_exp = models.IntegerField(default=0)
	phys_exp = models.IntegerField(default=0)
	chem_exp = models.IntegerField(default=0)
	life_exp = models.IntegerField(default=0)
	prog_exp = models.IntegerField(default=0)
	health = models.IntegerField(default=0)
	map = models.ForeignKey(Map, null=True)
	skill = models.ForeignKey(Skill)
	drop_rate = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
	dialog1 = models.CharField(max_length=50, default=u"dialog1")
	dialog2 = models.CharField(max_length=50, default=u"dialog2")
	dialog3 = models.CharField(max_length=50, default=u"dialog3")
	dialog4 = models.CharField(max_length=50, default=u"dialog4")
	dialog5 = models.CharField(max_length=50, default=u"dialog5")
	death_dialog = models.CharField(max_length=50, default=u"death dialog")

	def type(self):
		if self.math_exp > 0:
			return "math"
		elif self.phys_exp > 0:
			return "phys"
		elif self.chem_exp > 0:
			return "chem"
		elif self.life_exp > 0:
			return "life"
		elif self.prog_exp > 0:
			return "prog"

	def __str__(self):
		if self.math_exp > 0:
			category = u"[수학] "
			exp = self.math_exp
		elif self.phys_exp > 0:
			category = u"[물리] "
			exp = self.phys_exp
		elif self.chem_exp > 0:
			category = u"[화학] "
			exp = self.chem_exp
		elif self.life_exp > 0:
			category = u"[생물] "
			exp = self.life_exp
		elif self.prog_exp > 0:
			category = u"[프밍] "
			exp = self.prog_exp
		else:
			category = u"[????] "
			exp = 0
		
		return u"[" + self.map.name + u"]" + category + self.name + " (" + unicode(exp) + u", " + unicode(self.health) + u", " + unicode(self.skill.name) + u", " + unicode(self.drop_rate) + u"%)"

@python_2_unicode_compatible
class Battle(models.Model):
	character = models.OneToOneField(Character, on_delete=models.CASCADE)
	monster = models.ForeignKey(Monster)
	ally_health = models.IntegerField(default=100)
	enemy_health = models.IntegerField(default=0)
	turn = models.IntegerField(default=0)

	def __str__(self):
		return unicode(self.character)

@python_2_unicode_compatible
class Skillbook(models.Model):
	group = models.ForeignKey(Group)
	skill = models.ForeignKey(Skill)
	finder = models.ForeignKey(Character, on_delete=models.CASCADE)

	def __str__(self):
		return u"[" + unicode(self.group) + "] " + unicode(self.skill)

@python_2_unicode_compatible
class Monsterbook(models.Model):
	group = models.ForeignKey(Group)
	grade = models.ForeignKey(Grade, default=1)
	monster = models.ForeignKey(Monster)
	finder = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='finder')
	champion = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='champion')

	def __str__(self):
		return u"[" + unicode(self.group) + "] " + unicode(self.monster)

@python_2_unicode_compatible
class Bossmonster(models.Model):
	name = models.CharField(max_length=40)
	img = models.ImageField(upload_to='images/monster/', default='images/monster/default.png')
	health = models.IntegerField(default=100000)
	damage = models.IntegerField(default=10)
	map = models.ForeignKey(Map)
	skill = models.ForeignKey(Skill, null=True, blank=True)

	def __str__(self):
		return u"[" + self.map.name + u"] " + self.name + u"(" + unicode(self.health) + u")"

@python_2_unicode_compatible
class Bossmonsterbook(models.Model):
	group = models.ForeignKey(Group)
	grade = models.ForeignKey(Bossgrade, default=1)
	bossmonster = models.ForeignKey(Bossmonster)
	
	def __str__(self):
		return u"[" + unicode(self.group) + "] " + unicode(self.bossmonster)

@python_2_unicode_compatible
class Bossbattlemanager(models.Model):
	bossmonster = models.ForeignKey(Bossmonster, on_delete=models.CASCADE)
	enemy_health = models.IntegerField(default=100000)
	boss_type = models.CharField(max_length=10, null=True, blank=True)
	banned_type = models.CharField(max_length=10, null=True, blank=True)
	turn = models.IntegerField(default=0)
	state = models.CharField(max_length=20, default="waiting")
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	bossskill = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return self.group.group_name + u": " + self.bossmonster.name

@python_2_unicode_compatible
class Bossbattle(models.Model):
	character = models.OneToOneField(Character, on_delete=models.CASCADE)
	ally_health = models.IntegerField(default=100)
	skill = models.ForeignKey(Skill, null=True, blank=True)
	ready = models.BooleanField(default=False)
	turn = models.IntegerField(default=0)
	ready_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

	def __str__(self):
		return unicode(self.character)
