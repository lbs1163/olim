# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
from collections import Counter
import random
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def server_check(original_function):
	@wraps(original_function)
	def wrapper(*args, **kwargs):
		try:
			server = Server.objects.all()[0]
		except:
			return HttpResponse("Please check the server instance of DB")

		if not server.is_open:
			return render(args[0], 'rpg/close.html')
		else:
			return original_function(*args, **kwargs)
	return wrapper

@server_check
@login_required
def index(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		name = request.user.last_name + request.user.first_name
		stats = [character.math, character.phys, character.chem, character.life, character.prog]
		maximum = max(stats)
		if maximum < 10:
			maximum = 10
		return render(request, 'rpg/index.html', { 'name': name, 'character': character, 'maximum': maximum })

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

			hair = Hair.objects.all()[0]
			eye = Eye.objects.all()[0]
			clothes = Clothes.objects.all()[0]

			character = Character(user=user, group=code.group, hair=hair, eye=eye, clothes=clothes)
			skills = Skill.objects.all()
			character.skill1 = None
			character.skill2 = None
			character.skill3 = None
			character.skill4 = None
			character.save()

			login(request, user)
			return render(request, 'rpg/signupcomplete.html')
		else:
			return render(request, 'rpg/signup.html', { 'form': form })

@server_check
@login_required
def map(request):
	maps = Map.objects.all()
	return render(request, 'rpg/map.html', { 'maps': maps })

@server_check
@login_required
def battle(request):
	character = Character.objects.get(user=request.user.id)
	try:
		battle = Battle.objects.get(character=character)
	except ObjectDoesNotExist:
		map_id = request.GET.get('id', 1)
		map = Map.objects.get(id=map_id)
		
		if not map.is_open:
			map = Map.objects.filter(is_open=True)[0]

		monster = random.choice(Monster.objects.filter(map=map))
		battle = Battle(character=character, monster=monster, enemy_health = monster.health)
		battle.save()

	if request.method == 'GET':
		return render(request, 'rpg/battle.html', { 'battle': battle, 'character': character })
	elif request.method == 'POST':

		if request.POST.get('type', False) == 'runaway':
			battle.delete()
			return JsonResponse({'type': 'runawaySuccess'})
		
		skillid = request.POST['skillid']

		if skillid == "0":
			damage = random.randrange(1,5)
			skillname = u"발버둥치기"
			health_used = 5
		else:
			try:
				skill = Skill.objects.get(id=skillid)

				if character.skill1 != skill and character.skill2 != skill and character.skill3 != skill and character.skill4 != skill:
					return JsonResponse({'type': 'characterDoesNotHaveSkill'})

				skillname = skill.name

			except ObjectDoesNotExist:
				return JsonResponse({'type': 'skillDoesNotExist'})
			
			# calculate damage
			damage = skill.damage
			if skill.math:
				damage += character.math
			elif skill.phys:
				damage += character.phys
			elif skill.chem:
				damage += character.chem
			elif skill.life:
				damage += character.life
			elif skill.prog:
				damage += character.prog

			if battle.monster.math_exp != 0 and skill.math:
				damage *= 2
				double = True
			elif battle.monster.phys_exp != 0 and skill.phys:
				damage *= 2
				double = True
			elif battle.monster.chem_exp != 0 and skill.chem:
				damage *= 2
				double = True
			elif battle.monster.life_exp != 0 and skill.life:
				damage *= 2
				double = True
			elif battle.monster.prog_exp != 0 and skill.prog:
				damage *= 2
				double = True
			else:
				double = False

			health_used = skill.health

		if battle.ally_health < health_used:
			return JsonResponse({'type': 'healthNotEnough'})

		battle.ally_health -= health_used
		battle.enemy_health -= damage
		battle.turn += 1

		givenskill = None

		# battle win
		if battle.enemy_health <= 0:
			battle.enemy_health = 0
			character.math += battle.monster.math_exp
			character.phys += battle.monster.phys_exp
			character.chem += battle.monster.chem_exp
			character.life += battle.monster.life_exp
			character.prog += battle.monster.prog_exp
			character.save()
			dialog = battle.monster.death_dialog

			grades = Grade.objects.all().order_by('turn')

			for grade in grades:
				if battle.turn <= grade.turn:
					bookgrade = grade
					break

			num = random.randrange(1, 100)

			if num <= battle.monster.drop_rate:
				skill = battle.monster.skill
			else:
				normalskills = Skill.objects.filter(math=False, phys=False, chem=False, life=False, prog=False)
				skill = random.choice(normalskills)

			have, created = Have.objects.get_or_create(character=character, skill=skill)
			have.number += 1
			have.save()

			givenskill = skill.name

			try:
				skillbook = Skillbook.objects.get(group=character.group, skill=skill)
			except:
				skillbook = Skillbook(group=character.group, skill=skill, finder=character)
				skillbook.save()

			try:
				monsterbook = Monsterbook.objects.get(group=character.group, monster=battle.monster)
				if monsterbook.grade.turn > bookgrade.turn:
					monsterbook.grade = bookgrade
					monsterbook.champion = character
					monsterbook.save()
			except:
				monsterbook = Monsterbook(group=character.group, monster=battle.monster, grade=bookgrade, finder=character, champion=character)
				monsterbook.save()
		else:
			dialogs = [battle.monster.dialog1, battle.monster.dialog2, battle.monster.dialog3, battle.monster.dialog4, battle.monster.dialog5]
			dialog = random.choice(dialogs)
		
		battle.save()

		if battle.enemy_health == 0:
			battle.delete()
			return JsonResponse({'type': 'battleWin', 'double': double, 'skillname': givenskill, 'skill': skillname, 'health_used': health_used, 'damage': damage, 'monster': battle.monster.name, 'dialog': dialog, 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health})
		else:
			return JsonResponse({'type': 'battleOngoing', 'double': double, 'skill': skillname, 'health_used': health_used, 'damage': damage, 'monster': battle.monster.name, 'dialog': dialog, 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health})

@server_check
@login_required
def monsterbook(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		group = character.group
		mathmonsterlist = Monster.objects.filter(math_exp__gt=0)
		physmonsterlist = Monster.objects.filter(phys_exp__gt=0)
		chemmonsterlist = Monster.objects.filter(chem_exp__gt=0)
		lifemonsterlist = Monster.objects.filter(life_exp__gt=0)
		progmonsterlist = Monster.objects.filter(prog_exp__gt=0)
		monsterbooklist = Monsterbook.objects.filter(group=group)
		monsterbookmonsters = [monsterbook.monster for monsterbook in monsterbooklist]
		
		return render(request, 'rpg/monsterbook.html', {'group': group, 'mathmonsterlist': mathmonsterlist, 'physmonsterlist': physmonsterlist, 'chemmonsterlist': chemmonsterlist, 'lifemonsterlist': lifemonsterlist, 'progmonsterlist': progmonsterlist,'monsterbooklist': monsterbooklist, 'monsterbookmonsters': monsterbookmonsters})

@server_check
@login_required
def skillbook(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		skillbooks = Skillbook.objects.filter(group = character.group)
		skills = [skillbook.skill for skillbook in skillbooks]
		allSkills = Skill.objects.all()
		allSkillsWithBoolean = [{'skill': skill, 'is_owned': skill in skills} for skill in allSkills]
		allCombinations = Combination.objects.all()
		
		return render(request, 'rpg/skillbook.html', {'group': character.group, 'allSkillsWithBoolean': allSkillsWithBoolean, 'skillbooks': skillbooks, 'allCombinations': allCombinations})

@server_check
@login_required
def combination(request):
	character = Character.objects.get(user=request.user.id)
	haves = Have.objects.filter(character=character, number__gt=0).order_by('skill')

	if request.method == 'GET':
		return render(request, 'rpg/combination.html', {'haves': haves})

	elif request.method == 'POST':
		try:
			left_skill = Skill.objects.get(id=request.POST.get('left', False))
			right_skill = Skill.objects.get(id=request.POST.get('right', False))
		except:
			return JsonResponse({'type': 'skillDoesNotExist'})
		
		try:
			left_skill_have = Have.objects.get(character=character, skill=left_skill)
			if left_skill == right_skill:
				right_skill_have = left_skill_have
			else:
				right_skill_have = Have.objects.get(character=character, skill=right_skill)

			if left_skill_have.number == 0 or right_skill_have.number == 0:
				return JsonResponse({'type': 'characterDoesNotHaveSkill'})
		except:
			return JsonResponse({'type': 'characterDoesNotHaveSkill'})

		alreadyfailed = True

		try:
			failedCombination = FailedCombination.objects.get(group=character.group, skill001=left_skill, skill002=right_skill)
		except:
			try:
				failedCombination = FailedCombination.objects.get(group=character.group, skill001=right_skill, skill002=left_skill)
			except:
				alreadyfailed = False

		if alreadyfailed:
			return JsonResponse({'type': 'combinationAlreadyFailed'})

		try:
			combination = Combination.objects.get(skill01=left_skill, skill02=right_skill)
		except:
			try:
				combination = Combination.objects.get(skill01=right_skill, skill02=left_skill)
			except:	
				if request.POST.get('real', None) == "false":
					return JsonResponse({'type': 'combinationNotDiscoveredYet'})
				elif request.POST.get('real', None) == "true":
					left_skill_have.number -= 1
					right_skill_have.number -= 1
					left_skill_have.save()
					right_skill_have.save()

					failedCombination = FailedCombination(group=character.group, skill001=left_skill, skill002=right_skill)
					failedCombination.save()
					return JsonResponse({'type': 'combinationDoesNotExist'})

		new_skill = combination.new_skill

		try:
			Skillbook.objects.get(group=character.group, skill=new_skill)
		except:
			if request.POST.get('real', None) == "false":
				return JsonResponse({'type': 'combinationNotDiscoveredYet'})

			newSkillbook = Skillbook(group=character.group, skill=new_skill, finder=character)
			newSkillbook.save()
			firstDiscovery = True;
		else:
			if request.POST.get('real', None) == "false":
				return JsonResponse({'type': 'combinationPreview', 'newSkill': {'id': new_skill.id, 'name': new_skill.name}})
			firstDiscovery = False;

		if request.POST.get('real', None) == "true":
			left_skill_have.number -= 1
			right_skill_have.number -= 1
			left_skill_have.save()
			right_skill_have.save()
			new_have, created = Have.objects.get_or_create(character=character, skill=new_skill)
			new_have.number += 1
			new_have.save()

		return JsonResponse({'type': 'combinationSuccess', 'newSkill': {'id': new_skill.id, 'name': new_skill.name}, 'firstDiscovery': firstDiscovery})

@server_check
@login_required
def selectskill(request):
	character = Character.objects.get(user=request.user.id)
	contains = Contain.objects.filter(character=character).order_by('skill')
	skills = list(set([contain.skill for contain in contains]) - set([character.skill1, character.skill2, character.skill3, character.skill4]))

	if request.method == 'GET':
		try:
			battle = Battle.objects.get(character=character)
			return render(request, 'rpg/cannotselectskill.html')
		except:
			return render(request, 'rpg/selectskill.html', {'character': character, 'skills': skills})

	elif request.method == 'POST':
		try:
			battle = Battle.objects.get(character=character)
			return JsonResponse({'type': 'selectFailed'})
		except:
			pass

		if character.skill1 is not None:
			have, created = Have.objects.get_or_create(character=character, skill=character.skill1)
			have.number += 1
			have.save()
		if character.skill2 is not None:
			have, created = Have.objects.get_or_create(character=character, skill=character.skill2)
			have.number += 1
			have.save()
		if character.skill3 is not None:
			have, created = Have.objects.get_or_create(character=character, skill=character.skill3)
			have.number += 1
			have.save()
		if character.skill4 is not None:
			have, created = Have.objects.get_or_create(character=character, skill=character.skill4)
			have.number += 1
			have.save()

		def getSkillOrNone(skillstring, existingSkill):
			try:
				skill = Skill.objects.get(id=request.POST.get(skillstring, None))
				have = Have.objects.get(character=character, skill=skill)
				if have.number == 0:
					return None
				elif skill.math and character.math < skill.limit:
					return None
				elif skill.phys and character.phys < skill.limit:
					return None
				elif skill.chem and character.chem < skill.limit:
					return None
				elif skill.life and character.life < skill.limit:
					return None
				elif skill.prog and character.prog < skill.limit:
					return None
				else:
					have.number -= 1
					have.save()
					return skill
			except:
				return None

		character.skill1 = getSkillOrNone("skill1", character.skill1)
		character.skill2 = getSkillOrNone("skill2", character.skill2)
		character.skill3 = getSkillOrNone("skill3", character.skill3)
		character.skill4 = getSkillOrNone("skill4", character.skill4)

		character.save()

		return JsonResponse({'type': 'selectSuccess'})
