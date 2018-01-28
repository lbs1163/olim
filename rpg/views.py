# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
from collections import Counter
import random, datetime
from math import floor
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def calculate_damage(character, skill, monstertype):
	
	if skill == None:
		health_used = 5
		damage = 5
		realdamage = random.randrange(round(damage * 0.9), round(damage * 1.1))
		double = False
		return (realdamage, health_used, double)
	else:
		health_used = skill.health
		damage = skill.damage
	
	if skill.math or (skill.improvise and monstertype=="math"):
		damage += round((character.math - skill.limit) * 0.7)
	elif skill.phys or (skill.improvise and monstertype=="phys"):
		damage += round((character.phys - skill.limit) * 0.7)
	elif skill.chem or (skill.improvise and monstertype=="chem"):
		damage += round((character.chem - skill.limit) * 0.7)
	elif skill.life or (skill.improvise and monstertype=="life"):
		damage += round((character.life - skill.limit) * 0.7)
	elif skill.prog or (skill.improvise and monstertype=="prog"):
		damage += round((character.prog - skill.limit) * 0.7)

	if skill.type() == monstertype or skill.improvise:
		damage *= 2
		double = True
	else:
		double = False

	health_used = skill.health

	if round(damage * 0.9) == round(damage * 1.1):
		realdamage = round(damage * 0.9)
	else:
		realdamage = random.randrange(round(damage * 0.9), round(damage * 1.1))
	
	return (realdamage, health_used, double)

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
			print(code_used)
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
	maps = Map.objects.all().order_by("id")
	openmaps = Map.objects.filter(is_open=True).order_by("-id")
	exam = openmaps[0].name
	exam = exam[0:len(exam) - 2]
	return render(request, 'rpg/map.html', { 'maps': maps, 'exam': exam })

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
		percentage = battle.enemy_health * 100.0 / battle.monster.health
		return render(request, 'rpg/battle.html', { 'battle': battle, 'character': character, 'percentage': percentage })

	elif request.method == 'POST':

		if request.POST.get('type', False) == 'runaway':
			battle.delete()
			return JsonResponse({'type': 'runawaySuccess'})
		
		skillid = request.POST.get('skillid', "0")

		if skillid == "0":
			realdamage, health_used, double = calculate_damage(character, None, battle.monster.skill.type)
			skillname = u"발버둥치기"
		else:
			try:
				skill = Skill.objects.get(id=skillid)

				if character.skill1 != skill and character.skill2 != skill and character.skill3 != skill and character.skill4 != skill:
					return JsonResponse({'type': 'characterDoesNotHaveSkill'})

				skillname = skill.name

			except ObjectDoesNotExist:
				return JsonResponse({'type': 'skillDoesNotExist'})

			realdamage, health_used, double = calculate_damage(character, skill, battle.monster.type())

		if battle.ally_health < health_used:
			return JsonResponse({'type': 'healthNotEnough'})

		battle.ally_health -= health_used

		if battle.ally_health > 100:
			battle.ally_health = 100

		battle.enemy_health -= realdamage
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

			if battle.monster.math_exp:
				exp_type = u"수학"
				exp = battle.monster.math_exp
			elif battle.monster.phys_exp:
				exp_type = u"물리"
				exp = battle.monster.phys_exp
			elif battle.monster.chem_exp:
				exp_type = u"화학"
				exp = battle.monster.chem_exp
			elif battle.monster.life_exp:
				exp_type = u"생물"
				exp = battle.monster.life_exp
			elif battle.monster.prog_exp:
				exp_type = u"프밍"
				exp = battle.monster.prog_exp

			character.save()
			dialog = battle.monster.death_dialog

			grades = Grade.objects.all().order_by('turn')

			for grade in grades:
				if battle.turn <= grade.turn:
					bookgrade = grade
					break

			num = random.randrange(0, 2)

			if num == 0:
				skill = None
			else:
				num2 = random.randrange(1, 101)
				if num2 < battle.monster.drop_rate:
					skill = battle.monster.skill
				else:
					normalskills = Skill.objects.filter(math=False, phys=False, chem=False, life=False, prog=False, boss=False)
					combinations = Combination.objects.all()
					skillsWithComb = set([combination.new_skill for combination in combinations])
					normSkillsWithoutComb = list(set(normalskills) - skillsWithComb)
					skill = random.choice(normSkillsWithoutComb)

				have, created = Have.objects.get_or_create(character=character, skill=skill)
				have.number += 1
				have.save()

			if skill is not None:
				givenskill = skill.name
			else:
				givenskill = False

			if skill is not None:
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
			return JsonResponse({'type': 'battleWin', 'exp_type': exp_type, 'exp': exp, 'double': double, 'skillname': givenskill, 'skill': skillname, 'health_used': health_used, 'damage': realdamage, 'monster': battle.monster.name, 'dialog': dialog, 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health, 'monsterhealth': battle.monster.health})
		else:
			return JsonResponse({'type': 'battleOngoing', 'double': double, 'skill': skillname, 'health_used': health_used, 'damage': realdamage, 'monster': battle.monster.name, 'dialog': dialog, 'ally_health': battle.ally_health, 'enemy_health': battle.enemy_health, 'monsterhealth': battle.monster.health})

@server_check
@login_required
def bossbattle(request):

	character = Character.objects.get(user=request.user.id)
	mybossbattle, _ = Bossbattle.objects.get_or_create(character=character)
	try:
		bossbattlemanager = Bossbattlemanager.objects.filter(group=character.group).order_by("-start_time")[0]
	except:
		map = Map.objects.filter(is_open=True).order_by("-id")[0]
		bossmonster = Bossmonster.objects.get(map=map)
		bossbattlemanager = Bossbattlemanager.objects.create(group=character.group, bossmonster=bossmonster)
		codes = RegistrationCode.objects.filter(group=character.group)
		bossbattlemanager.enemy_health = bossmonster.health * len(codes)
		bossbattlemanager.boss_type = random.choice(["math", "phys", "chem", "life", "prog"])
		bossbattlemanager.save()

	if request.method == 'GET':
		if bossbattlemanager.state == "ready":
			codes = RegistrationCode.objects.filter(group=character.group)
			characters = Character.objects.filter(group=character.group)
			percentage = bossbattlemanager.enemy_health * len(codes) * 100 / bossbattlemanager.bossmonster.health
			return render(request, 'rpg/bossbattle.html', {'bossbattlemanager': bossbattlemanager, 'bossbattle': mybossbattle, 'character': character, 'characters': characters, 'percentage': percentage})
		elif bossbattlemanager.state == "waiting":
			return render(request, 'rpg/getready.html', {'bossbattle': mybossbattle, 'bossbattlemanager': bossbattlemanager})
		else:
			map = Map.objects.filter(is_open=True).order_by("-id")[0]
			bossmonster = Bossmonster.objects.get(map=map)
			bossbattlemanager = Bossbattlemanager.objects.create(group=character.group, bossmonster=bossmonster)
			codes = RegistrationCode.objects.filter(group=character.group)
			bossbattlemanager.enemy_health = bossmonster.health * len(codes)
			bossbattlemanager.save()
			return render(request, 'rpg/getready.html', {'bossbattle': mybossbattle, 'bossbattlemanager': bossbattlemanager})


	elif request.method == 'POST':
		characters = Character.objects.filter(group=character.group)
		threshold = timezone.now() - datetime.timedelta(seconds=5)
		bossbattles = Bossbattle.objects.filter(character__in=characters, ready_time__gt=threshold)

		if request.POST.get("type", False) == 'ready':
			mybossbattle.ready = True
			mybossbattle.save()

			return JsonResponse({'numOfReady': len(bossbattles.filter(ready=True)), 'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'unready':
			mybossbattle.ready = False
			mybossbattle.save()
			return JsonResponse({'numOfReady': len(bossbattles.filter(ready=True)), 'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'refresh':
			mybossbattle.ready_time = timezone.now()
			mybossbattle.save()
			
			if len(bossbattles) == len(bossbattles.filter(ready=True)) and len(bossbattles) != 0:
				bossbattlemanager.state = "ready"
				bossbattlemanager.boss_type = random.choice(["math", "phys", "chem", "life", "prog"])
				bossbattlemanager.start_time = timezone.now()
				bossbattlemanager.save()
			
			return JsonResponse({'numOfReady': len(bossbattles.filter(ready=True)), 'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'attack':

			if request.POST.get("turn", False) == unicode(bossbattlemanager.turn):

				if request.POST.get("skill", False) == 'skill1':
					skill = character.skill1
				elif request.POST.get("skill", False) == 'skill2':
					skill = character.skill2
				elif request.POST.get("skill", False) == 'skill3':
					skill = character.skill3
				elif request.POST.get("skill", False) == 'skill4':
					skill = character.skill4
				else:
					skill = None

				if skill != None and bossbattlemanager.banned_type == skill.type:
					return JsonResponse({"type": "typeBanned", "turn": bossbattlemanager.turn})
				elif skill != None and skill.health > mybossbattle.ally_health:
					return JsonResponse({"type": "healthNotEnough", "turn": bossbattlemanager.turn})

				mybossbattle.skill = skill
				mybossbattle.save()

				return JsonResponse({"type": "attackSuccess", "turn": bossbattlemanager.turn})

			else:
				return JsonResponse({"type": "turnMismatch", "turn": bossbattlemanager.turn})

		elif request.POST.get("type", False) == 'everyonesecond':

			if bossbattlemanager.state != "ready":
				return JsonResponse({"type": bossbattlemanager.state, "givenskill": bossbattlemanager.bossmonster.skill.name, "monster": bossbattlemanager.bossmonster.name, "turn": bossbattlemanager.turn, "enemy_health": bossbattlemanager.enemy_health})

			if request.POST.get("turn", False) == unicode(bossbattlemanager.turn):
				if bossbattlemanager.start_time + datetime.timedelta(seconds=15) < timezone.now():
					bossbattlemanager.start_time = timezone.now()
					bossbattlemanager.save()

					characters = Character.objects.filter(group=character.group)
					bossbattles = Bossbattle.objects.filter(character__in=characters)

					for bossbattle in bossbattles:
						skill = bossbattle.skill
						bossbattle.skill = None

						if skill != None:
							realdamage, health_used, _ = calculate_damage(bossbattle.character, skill, bossbattlemanager.boss_type)
						else:
							realdamage = 0
							health_used = 0
	
						bossbattlemanager.enemy_health -= realdamage
						bossbattle.ally_health -= health_used
						if bossbattle.ally_health > 100:
							bossbattle.ally_health = 100
						bossbattle.save()
	
					if bossbattlemanager.enemy_health <= 0:
						
						bossgrades = Bossgrade.objects.all().order_by('turn')

						for bossgrade in bossgrades:
							if bossbattlemanager.turn + 1 <= bossgrade.turn:
								bookgrade = bossgrade
								break;

						chs = Character.objects.filter(group=character.group)
						for ch in chs:
							have, created = Have.objects.get_or_create(skill=bossbattlemanager.bossmonster.skill, character=ch)
							have.number += 1
							have.save()

						Skillbook.objects.get_or_create(group=character.group, skill=bossbattlemanager.bossmonster.skill, finder=character)

						try:
							bossmonsterbook = Bossmonsterbook.objects.get(group=character.group, bossmonster=bossbattlemanager.bossmonster)
							if bossmonsterbook.grade.turn > bookgrade.turn:
								bossmonsterbook.grade = bookgrade
								bossmonsterbook.save()
						except:
							Bossmonsterbook.objects.create(group=character.group, bossmonster=bossbattlemanager.bossmonster, grade=bookgrade)
							
						for bossbattle in bossbattles:
							bossbattle.delete()
						bossbattlemanager.state = "win"
						bossbattlemanager.turn += 1
						bossbattlemanager.save()
						return JsonResponse({"type": "win", "givenskill": bossbattlemanager.bossmonster.skill.name, "monster": bossbattlemanager.bossmonster.name, "turn": bossbattlemanager.turn, "enemy_health": bossbattlemanager.enemy_health})

					elif bossbattlemanager.turn + 1 >= 20:
						
						bossgrade = Bossgrade.objects.all().order_by('-turn')[0]

						try:
							bossmonsterbook = Bossmonsterbook.objects.get(group=character.group, bossmonster=bossbattlemanager.bossmonster)
						except:
							Bossmonsterbook.objects.create(group=character.group, bossmonster=bossbattlemanager.bossmonster, grade=bossgrade)

						for bossbattle in bossbattles:
							bossbattle.delete()
						bossbattlemanager.state = "lose"
						bossbattlemanager.turn += 1
						bossbattlemanager.save()
						return JsonResponse({"type": "lose", "monster": bossbattlemanager.bossmonster.name, "turn": bossbattlemanager.turn, "enemy_health": bossbattlemanager.enemy_health})
	
					maps = Map.objects.filter(is_open=True)
					bossskill = random.randrange(0, len(maps))
					#bossskill = 3
				
					if bossskill == 0:
						while True:
							type = random.choice(["math", "phys", "chem", "life", "prog"])
							if type != bossbattlemanager.boss_type:
								break
						bossbattlemanager.boss_type = type
						bossbattlemanager.save()
					elif bossskill == 1:
						for bossbattle in bossbattles:
							bossbattle.ally_health -= bossbattlemanager.bossmonster.damage
							if bossbattle.ally_health < 0:
								bossbattle.ally_health = 0
							bossbattle.save()
					elif bossskill == 2:
						while True:
							type = random.choice(["math", "phys", "chem", "life", "prog"])
							if type != bossbattlemanager.banned_type:
								break
						bossbattlemanager.banned_type = type
						bossbattlemanager.save()
					elif bossskill == 3:
						lives = Bossbattle.objects.filter(character__group=character.group, ally_health__gt=0).order_by('?')
						halflives = lives[0:len(lives)/2]
						for randbossbattle in halflives:
							randbossbattle.ally_health = 0
							randbossbattle.save()

					bossbattlemanager.bossskill = bossskill
					bossbattlemanager.turn += 1
					bossbattlemanager.save()

			codes = RegistrationCode.objects.filter(group=character.group)
			monsterhealth = len(codes) * bossbattlemanager.bossmonster.health

			mybossbattle = Bossbattle.objects.get(character=character)

			return JsonResponse({"type": "everyonesecond", "bossskill": bossbattlemanager.bossskill, "bosstype": bossbattlemanager.boss_type, "bossdamage": bossbattlemanager.bossmonster.damage, "bannedtype": bossbattlemanager.banned_type, "monster": bossbattlemanager.bossmonster.name, "turn": bossbattlemanager.turn, "ally_health": mybossbattle.ally_health, "enemy_health": bossbattlemanager.enemy_health, "monsterhealth": monsterhealth})

@server_check
@login_required
def monsterbook(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		group = character.group
		mathmonsterlist = Monster.objects.filter(math_exp__gt=0).order_by('health')
		physmonsterlist = Monster.objects.filter(phys_exp__gt=0).order_by('health')
		chemmonsterlist = Monster.objects.filter(chem_exp__gt=0).order_by('health')
		lifemonsterlist = Monster.objects.filter(life_exp__gt=0).order_by('health')
		progmonsterlist = Monster.objects.filter(prog_exp__gt=0).order_by('health')
		monsterbooklist = Monsterbook.objects.filter(group=group)
		monsterbookmonsters = [monsterbook.monster for monsterbook in monsterbooklist]
		bossmonsterlist = Bossmonster.objects.all().order_by('health')
		bossmonsterbooklist = Bossmonsterbook.objects.filter(group=group)
		bossmonsterbookmonsters = [bossmonsterbook.bossmonster for bossmonsterbook in bossmonsterbooklist]
		
		return render(request, 'rpg/monsterbook.html', {'group': group, 'mathmonsterlist': mathmonsterlist, 'physmonsterlist': physmonsterlist, 'chemmonsterlist': chemmonsterlist, 'lifemonsterlist': lifemonsterlist, 'progmonsterlist': progmonsterlist,'monsterbooklist': monsterbooklist, 'monsterbookmonsters': monsterbookmonsters, 'bossmonsterlist': bossmonsterlist, 'bossmonsterbooklist': bossmonsterbooklist, 'bossmonsterbookmonsters': bossmonsterbookmonsters})

@server_check
@login_required
def skillbook(request):
	if request.method == 'GET':
		character = Character.objects.get(user=request.user.id)
		skillbooks = Skillbook.objects.filter(group = character.group)
		skills = [skillbook.skill for skillbook in skillbooks]
		allSkills = Skill.objects.all().order_by('damage')
		allSkillsWithBoolean = [{'skill': skill, 'is_owned': skill in skills} for skill in allSkills]
		allCombinations = Combination.objects.all()
		
		return render(request, 'rpg/skillbook.html', {'group': character.group, 'allSkillsWithBoolean': allSkillsWithBoolean, 'skillbooks': skillbooks, 'allCombinations': allCombinations})

@server_check
@login_required
def combination(request):
	character = Character.objects.get(user=request.user.id)
	haves = Have.objects.filter(character=character, number__gt=0, skill__boss=False).order_by('skill')

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
	haves = Have.objects.filter(character=character, number__gt=0).order_by('skill')
	skills = list(set([have.skill for have in haves]) - set([character.skill1, character.skill2, character.skill3, character.skill4]))

	if request.method == 'GET':
		try:
			battle = Battle.objects.get(character=character)
			return render(request, 'rpg/cannotselectskill.html')
		except:
			try:
				bossbattlemanager = Bossbattlemanager.objects.filter(group=character.group, state="ready")[0]
				return render(request, 'rpg/cannotselectskill.html')
			except:
				return render(request, 'rpg/selectskill.html', {'character': character, 'skills': skills})

	elif request.method == 'POST':
		try:
			battle = Battle.objects.get(character=character)
			return JsonResponse({'type': 'selectFailed'})
		except:
			try:
				bossbattlemanager = Bossbattlemanager.objects.filter(group=character.group, state="ready")[0]
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
