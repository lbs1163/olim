# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(RegistrationCode)
admin.site.register(Hair)
admin.site.register(Eye)
admin.site.register(Clothes)
admin.site.register(Character)
admin.site.register(Skill)
admin.site.register(Monster)
admin.site.register(Battle)
admin.site.register(Monsterbook)
admin.site.register(Skillbook)
admin.site.register(Map)
admin.site.register(Combination)
admin.site.register(FailedCombination)
admin.site.register(Server)
admin.site.register(Grade)
admin.site.register(Bossgrade)
admin.site.register(Have)
admin.site.register(Bossmonster)
admin.site.register(Bossbattlemanager)
admin.site.register(Bossbattle)
admin.site.register(Bossmonsterbook)
admin.site.register(Finalbossbattle)
admin.site.register(Finalbossbattlemanager)