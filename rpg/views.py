# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def index(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		name = request.user.last_name + request.user.first_name
		return render(request, 'rpg/index.html', { 'name': name, 'eye': character.eye, 'hair': character.hair, 'clothes': character.clothes })

def signup(request):
	if request.method == 'GET':
		form = SignupForm()
		return render(request, 'rpg/signup.html', { 'form': form })
	elif request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			code_used = form.cleaned_data.get('registration_code')
			code = RegistrationCode.objects.filter(code=code_used)[0]
			code.is_used = True
			code.save()

			user.first_name = code.first_name
			user.last_name = code.last_name
			user.save()

			character = Character(user=user, group=code.group)
			character.save()

			login(request, user)
			return render(request, 'rpg/signupcomplete.html')
		else:
			return render(request, 'rpg/signup.html', { 'form': form })

@login_required
def battle(request):
	character = Character.objects.get(user=request.user.id)
	try:
		battle = Battle.objects.get(character=character)
	except ObjectDoesNotExist:
		monster = Monster.objects.all()[0]
		battle = Battle(character=character, monster=monster)
		battle.save()

	if request.method == 'GET':
		return render(request, 'rpg/battle.html', { 'battle': battle, 'character': character })
	elif request.method == 'POST':
		skillid = request.POST['skillid']
		try:
			skill = Skill.objects.get(id=skillid)
		except ObjectDoesNotExist:
			return JsonResponse({'monster': battle.monster.name, 'dialog': u"뭔가 잘못되었다", 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health})

		damage = skill.damage
		health_used = skill.health
		battle.ally_health -= health_used
		battle.enemy_health += damage
		if battle.enemy_health > 100:
			battle.enemy_health = 100
		dialogs = [battle.monster.dialog1, battle.monster.dialog2, battle.monster.dialog3]
		dialog = random.choice(dialogs)
		battle.save()

		if battle.enemy_health == 100:
			battle_win = True
			battle.delete()
		else:
			battle_win = False

		return JsonResponse({'battle_win': battle_win, 'skill': skill.name, 'health_used': health_used, 'damage': damage, 'monster': battle.monster.name, 'dialog': dialog, 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health})

@login_required
def monsterbook(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		group = character.group
		monsterlist = Monster.objects.all()
		monsterbooklist = Monsterbook.objects.filter(group=group)
		monsterbooknamelist = [monsterbook.monster.name for monsterbook in monsterbooklist]
		found = 0

		return render(request, 'rpg/monsterbook.html', {'group': group, 'monsterlist': monsterlist, 'monsterbooklist': monsterbooklist, 'monsterbooknamelist': monsterbooknamelist, 'found': found})
