# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
from collections import Counter
import random, datetime#, operator
from math import floor
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q

# Create your views here.

def server_check(original_function):
	@wraps(original_function)
	def wrapper(*args, **kwargs):
		try:
			server = Server.objects.all().order_by('id')[0]
		except:
			return HttpResponse("Please check the server instance of DB")

		if not server.is_open:
			return render(args[0], 'rpg/close.html')
		else:
			return original_function(*args, **kwargs)
	return wrapper

def final_boss_check(original_function):
	@wraps(original_function)
	def wrapper(*args, **kwargs):
		try:
			server = Server.objects.all().order_by('id')[1]
		except:
			return HttpResponse("Please check the server instance of DB")

		if server.is_open:
			return redirect('finalbossbattle')
		else:
			return original_function(*args, **kwargs)
	return wrapper

@login_required
def codemenu(request):
	if request.user.is_staff:
		codes = Code.objects.all()
		return render(request, 'rpg/codemenu.html', {'codes': codes})
	else:
		return redirect('index')

@login_required
def day1(request):
	if request.user.is_staff:
		return render(request, 'rpg/day1.html')
	else:
		return redirect('index')

@login_required
def day2(request):
	if request.user.is_staff:
		return render(request, 'rpg/day2.html')
	else:
		return redirect('index')

@login_required
def day3(request):
	if request.user.is_staff:
		return render(request, 'rpg/day3.html')
	else:
		return redirect('index')

@login_required
def day4(request):
	if request.user.is_staff:
		return render(request, 'rpg/day4.html')
	else:
		return redirect('index')

@login_required
@final_boss_check
def code(request):
	character = Character.objects.get(user=request.user.id)
	if request.method == 'GET':
		return render(request, 'rpg/code.html')
	elif request.method == 'POST':
		codetext = request.POST.get('code', False)

		try:
			code = Code.objects.get(code=codetext)
		except:
			return JsonResponse({'type': 'doesNotExist'})

		if code.hair:
			hairhave, created = Hairhave.objects.get_or_create(group=character.group, hair=code.hair)
			if created:
				return JsonResponse({'type': 'success', 'name': code.hair.name, 'img': code.hair.img.url})
			else:
				return JsonResponse({'type': 'alreadyHave', 'name': code.hair.name, 'img': code.hair.img.url})

		if code.eye:
			eyehave, created = Eyehave.objects.get_or_create(group=character.group, eye=code.eye)
			if created:
				return JsonResponse({'type': 'success', 'name': code.eye.name, 'img': code.eye.img.url})
			else:
				return JsonResponse({'type': 'alreadyHave', 'name': code.eye.name, 'img': code.eye.img.url})
		
		if code.clothes:
			clotheshave, created = Clotheshave.objects.get_or_create(group=character.group, clothes=code.clothes)
			if created:
				return JsonResponse({'type': 'success', 'name': code.clothes.name, 'img': code.clothes.img.url})
			else:
				return JsonResponse({'type': 'alreadyHave', 'name': code.clothes.name, 'img': code.clothes.img.url})

@server_check
@login_required
@final_boss_check
def custom(request):
	character = Character.objects.get(user=request.user.id)
	hairhaves = Hairhave.objects.filter(group=character.group)
	eyehaves = Eyehave.objects.filter(group=character.group)
	clotheshaves = Clotheshave.objects.filter(group=character.group)

	if request.method == 'GET':
		return render(request, 'rpg/custom.html', {'character': character, 'hairhaves': hairhaves, 'eyehaves': eyehaves, 'clotheshaves': clotheshaves})
	elif request.method == 'POST':
		hairhaveid = request.POST.get("hairhaveid", False)
		eyehaveid = request.POST.get("eyehaveid", False)
		clotheshaveid = request.POST.get("clotheshaveid", False)

		try:
			hairhave = Hairhave.objects.get(group=character.group, id=hairhaveid)
			character.hair = hairhave.hair
		except:
			pass

		try:
			eyehave = Eyehave.objects.get(group=character.group, id=eyehaveid)
			character.eye = eyehave.eye
		except:
			pass

		try:
			clotheshave = Clotheshave.objects.get(group=character.group, id=clotheshaveid)
			character.clothes = clotheshave.clothes
		except:
			pass

		character.save()
		return JsonResponse({'type': 'customSuccess'})

def ending(request):
	if request.method == 'GET':
		return HttpResponse(u"엔딩 크레딧 아직 구현하지 못했습니다 호호호호호호");

def get_skill(character, skillnum):
	if skillnum == 'skill1':
		skill = character.skill1
	elif skillnum == 'skill2':
		skill = character.skill2
	elif skillnum == 'skill3':
		skill = character.skill3
	elif skillnum == 'skill4':
		skill = character.skill4
	else:
		skill = None

	return skill

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

def give_exp(battle):
	battle.character.math += battle.monster.math_exp
	battle.character.phys += battle.monster.phys_exp
	battle.character.chem += battle.monster.chem_exp
	battle.character.life += battle.monster.life_exp
	battle.character.prog += battle.monster.prog_exp

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

	battle.character.save()

	return (exp_type, exp)

def make_skillbook(character, skill):
	if skill is not None:
		try:
			skillbook = Skillbook.objects.get(group=character.group, skill=skill)
		except:
			skillbook = Skillbook(group=character.group, skill=skill, finder=character)
			skillbook.save()

def give_skill(battle):
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

		have, created = Have.objects.get_or_create(character=battle.character, skill=skill)
		have.number += 1
		have.save()
	
	return skill

def make_monsterbook(battle):

	grades = Grade.objects.all().order_by('turn')

	for grade in grades:
		if battle.turn <= grade.turn:
			bookgrade = grade
			break

	try:
		monsterbook = Monsterbook.objects.get(group=battle.character.group, monster=battle.monster)
		if monsterbook.grade.turn > bookgrade.turn:
			monsterbook.grade = bookgrade
			monsterbook.champion = battle.character
			monsterbook.save()
	except:
		monsterbook = Monsterbook(group=battle.character.group, monster=battle.monster, grade=bookgrade, finder=battle.character, champion=battle.character)
		monsterbook.save()

def calculate_boss_damage(bossbattles, bossbattlemanager):
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

def give_boss_skills(group, skill):

	chs = Character.objects.filter(group=group)
	for ch in chs:
		have, created = Have.objects.get_or_create(skill=skill, character=ch)
		have.number += 1
		have.save()

	Skillbook.objects.get_or_create(group=group, skill=skill)

def make_bossmonsterbook(bossbattlemanager):
	bossgrades = Bossgrade.objects.all().order_by('turn')

	for bossgrade in bossgrades:
		if bossbattlemanager.turn + 1 <= bossgrade.turn:
			bookgrade = bossgrade
			break;

	try:
		bossmonsterbook = Bossmonsterbook.objects.get(group=bossbattlemanager.group, bossmonster=bossbattlemanager.bossmonster)
		if bossmonsterbook.grade.turn > bookgrade.turn:
			bossmonsterbook.grade = bookgrade
			bossmonsterbook.save()
	except:
		Bossmonsterbook.objects.create(group=bossbattlemanager.group, bossmonster=bossbattlemanager.bossmonster, grade=bookgrade)

def delete_bossbattles(bossbattlemanager, bossbattles, state):
	for bossbattle in bossbattles:
		bossbattle.delete()
	bossbattlemanager.state = state
	bossbattlemanager.turn += 1
	bossbattlemanager.save()

def boss_attack(bossbattlemanager, bossbattles):

	maps = Map.objects.filter(is_open=True)
	bossskill = random.randrange(0, len(maps))	

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
		type = bossbattlemanager.boss_type
		bossbattlemanager.banned_type = type
		bossbattlemanager.save()

	elif bossskill == 3:
		lives = Bossbattle.objects.filter(character__group=bossbattlemanager.group, ally_health__gt=0).order_by('?')
		halflives = lives[0:len(lives)/2]
		for randbossbattle in halflives:
			randbossbattle.ally_health = 0
			randbossbattle.save()

	return bossskill

@login_required
def finalbossbattle(request):
	character = Character.objects.get(user=request.user.id)
	myfinalbossbattle, _ = Finalbossbattle.objects.get_or_create(character=character)
	characters = Character.objects.all()
	for cha in characters:
		Finalbossbattle.objects.get_or_create(character=cha)
	finalbossbattlemanager, created = Finalbossbattlemanager.objects.get_or_create()
	if created:
		codes = RegistrationCode.objects.all()
		finalbossbattlemanager.enemy_health = len(codes) * 200000
		finalbossbattlemanager.save()
	
	if request.method == 'GET':
		if request.user.is_staff:
			codes = RegistrationCode.objects.all()
			percentage = finalbossbattlemanager.enemy_health * 100 / (len(codes) * 200000)
			return render(request, 'rpg/finalbossbattle.html', { 'finalbossbattlemanager': finalbossbattlemanager, 'percentage': percentage })
		else:
			server = Server.objects.all().order_by('id')[1]
			if server.is_open:
				return render(request, 'rpg/finalbossbattlecommander.html', {
					'finalbossbattle': myfinalbossbattle,
					'character': character,
					'finalbossbattlemanager': finalbossbattlemanager})
			else:
				return redirect('index')
	
	elif request.method == 'POST':
		if request.user.is_staff:
			if request.POST.get('type', False) == "ready":
				finalbossbattles = Finalbossbattle.objects.filter(character__user__is_staff=False, frusted=False)
				for finalbossbattle in finalbossbattles:
					finalbossbattle.ready = True
					finalbossbattle.save()
				return JsonResponse({'state': finalbossbattlemanager.state})
			if request.POST.get('type', False) == "finalbattle":
				finalbossbattlemanager.state = "finalbattle"
				finalbossbattlemanager.save()
				return JsonResponse({'state': finalbossbattlemanager.state})
			elif request.POST.get('type', False) == "ending":
				finalbossbattlemanager.state = "ending"
				finalbossbattlemanager.save()
				return JsonResponse({'state': finalbossbattlemanager.state})
			elif request.POST.get('type', False) == "getDamage":
				enemy_health = finalbossbattlemanager.enemy_health;
				codes = RegistrationCode.objects.all()
				monsterhealth = len(codes) * 200000
				return JsonResponse({'state': finalbossbattlemanager.state, 'enemy_health': enemy_health, 'monsterhealth': monsterhealth})
			elif request.POST.get('type', False) == "calculate":
				finalbossbattles = Finalbossbattle.objects.all()
				for finalbossbattle in finalbossbattles:
					finalbossbattle.ready = False
					finalbossbattle.save()
				codes = RegistrationCode.objects.all()
				monsterhealth = len(codes) * 200000

				notfrusteds = Finalbossbattle.objects.filter(frusted=False, helper=None, character__user__is_staff=False).order_by('?')
				
				frustednumber = len(Finalbossbattle.objects.filter(frusted=True, character__user__is_staff=False))
				if frustednumber == 0 and finalbossbattlemanager.state == "helpeachother":
					finalbossbattlemanager.state = "helpphoenix"
					finalbossbattlemanager.save()
					return JsonResponse({'type': "helpphoenix"})

				elif len(notfrusteds) == 1 and finalbossbattlemanager.state == "finalbattle":
					finalbossbattlemanager.state = "allfrusted"
					finalbossbattlemanager.save()
					frustednumber = len(Finalbossbattle.objects.filter(frusted=True))
					return JsonResponse({
						'state': "finalbattle",
						'type': "allfrusted",
						'frustednumber': frustednumber,
						'enemy_health': finalbossbattlemanager.enemy_health,
						'monsterhealth': monsterhealth})

				notfrusteds = notfrusteds[:len(notfrusteds)/2]

				for notfrusted in notfrusteds:
					notfrusted.frusted = True
					notfrusted.save()

				frustednumber = len(Finalbossbattle.objects.filter(frusted=True))
				return JsonResponse({
					'type': "ongoing",
					'frustednumber': frustednumber,
					'enemy_health': finalbossbattlemanager.enemy_health,
					'monsterhealth': monsterhealth})
			elif request.POST.get('type', False) == "helpeachother":
				finalbossbattlemanager.state = "helpeachother"
				finalbossbattlemanager.save()
				return JsonResponse({'state': finalbossbattlemanager.state})
			elif request.POST.get('type', False) == "finalattack":
				finalbossbattlemanager.state = "finalattack"
				finalbossbattlemanager.save()
				return JsonResponse({'state': finalbossbattlemanager.state})
			return JsonResponse({'state': finalbossbattlemanager.state})

		else:
			if request.POST.get('type', False) == "everyonesecond":
				return JsonResponse({
					'state': finalbossbattlemanager.state,
					'ally_health': myfinalbossbattle.ally_health,
					'ready': myfinalbossbattle.ready,
					'frusted': myfinalbossbattle.frusted,
					'helper': unicode(myfinalbossbattle.helper)})

			elif request.POST.get('type', False) == "help":
				if finalbossbattlemanager.state == "helpphoenix":
					myfinalbossbattle.ready = False
					myfinalbossbattle.save()
					return JsonResponse({'type': 'helped'})
				if myfinalbossbattle.ready:
					myfinalbossbattle.ready = False
					myfinalbossbattle.save()
					
					if myfinalbossbattle.frusted:
						return JsonResponse({'type': 'frusted'})
					try:
						frusted = Finalbossbattle.objects.filter(frusted=True).order_by('?')[0]
						frusted.frusted = False
						frusted.helper = character
						frusted.save()
						return JsonResponse({'type': 'helped'})
					except:
						return JsonResponse({'type': 'noFrusted'})
				else:
					return JsonResponse({'type': 'helped'})

			elif request.POST.get('type', False) == "attack":
				if myfinalbossbattle.ready:
					if finalbossbattlemanager.state != 'finalattack':
						myfinalbossbattle.ready = False
					myfinalbossbattle.save()

					if myfinalbossbattle.frusted:
						return JsonResponse({'type': 'frusted'})

					if finalbossbattlemanager.state != 'finalbattle' and finalbossbattlemanager.state != 'finalattack':
						myfinalbossbattle.ready = True
						myfinalbossbattle.save()
						return JsonResponse({'type': 'time2help'})

					skill = get_skill(character, request.POST.get('skill', False))

					if skill == None:
						realdamage = 0
						health_used = 0
					else:
						realdamage, health_used, _ = calculate_damage(character, skill, "normal")

					if myfinalbossbattle.ally_health < health_used and finalbossbattlemanager.state != 'finalattack':
						myfinalbossbattle.ready = True
						myfinalbossbattle.save()
						return JsonResponse({'type': 'healthNotEnough'})

					if finalbossbattlemanager.state != 'finalattack':
						myfinalbossbattle.ally_health -= health_used
					finalbossbattlemanager.enemy_health -= realdamage

					if myfinalbossbattle.ally_health > 100:
						myfinalbossbattle.ally_health = 100

					if finalbossbattlemanager.enemy_health < 0:
						finalbossbattlemanager.enemy_health = 0

					myfinalbossbattle.save()
					finalbossbattlemanager.save()

					return JsonResponse({'type': 'attackSuccess'})
				else:
					return JsonResponse({'type': 'attackFailure'})

@server_check
@login_required
@final_boss_check
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

			hairhaves = Hairhave.objects.filter(group=code.group).order_by('?')
			eyehaves = Eyehave.objects.filter(group=code.group).order_by('?')
			clotheshaves = Clotheshave.objects.filter(group=code.group).order_by('?')
			hair = hairhaves[0].hair
			eye = eyehaves[0].eye
			clothes = clotheshaves[0].clothes

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
@final_boss_check
def map(request):
	maps = Map.objects.all().order_by("id")
	openmaps = Map.objects.filter(is_open=True).order_by("-id")
	exam = openmaps[0].name
	exam = exam[0:len(exam) - 2]
	return render(request, 'rpg/map.html', { 'maps': maps, 'exam': exam })

@server_check
@login_required
@final_boss_check
def battle(request):
	character = Character.objects.get(user=request.user.id)
	try:
		battle = Battle.objects.get(character=character)
	except ObjectDoesNotExist:
		if character.battletime == None or character.battletime < (timezone.now() - datetime.timedelta(seconds=10)):
			map_id = request.GET.get('id', 1)
			map = Map.objects.get(id=map_id)
			
			if not map.is_open:
				map = Map.objects.filter(is_open=True)[0]
	
			monster = random.choice(Monster.objects.filter(map=map))
			character.battletime = timezone.now()
			character.save()
			battle = Battle(character=character, monster=monster, enemy_health = monster.health)
			battle.save()
		else:
			return render(request, 'rpg/wait10seconds.html');

	if request.method == 'GET':
		percentage = battle.enemy_health * 100.0 / battle.monster.health
		message = Message.objects.all().order_by('?')[0]
		return render(request, 'rpg/battle.html', { 'battle': battle, 'character': character, 'percentage': percentage, 'message': message.text })

	elif request.method == 'POST':

		if request.POST.get('type', False) == 'runaway':
			battle.delete()
			return JsonResponse({'type': 'runawaySuccess'})

		skill = get_skill(character, request.POST.get('skill', False))

		if skill == None:
			realdamage, health_used, double = calculate_damage(character, None, battle.monster.type())
			skillname = u"발버둥치기"
		else:
			realdamage, health_used, double = calculate_damage(character, skill, battle.monster.type())
			skillname = skill.name

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

			exp_type, exp = give_exp(battle)
			skill = give_skill(battle)
			make_skillbook(character, skill)
			make_monsterbook(battle)

			character.group.kill += 1
			character.group.save()

			if skill != None:
				givenskill = skill.name
			else:
				givenskill = False

			dialog = battle.monster.death_dialog

		else:
			dialogs = [battle.monster.dialog1, battle.monster.dialog2, battle.monster.dialog3, battle.monster.dialog4, battle.monster.dialog5]
			dialog = random.choice(dialogs)
		
		battle.save()

		if battle.enemy_health == 0:
			battle.delete()
			return JsonResponse({
				'type': 'battleWin',
				'exp_type': exp_type,
				'exp': exp,
				'double': double,
				'skillname': givenskill,
				'skill': skillname,
				'health_used': health_used,
				'damage': realdamage,
				'monster': battle.monster.name,
				'dialog': dialog,
				'ally_health': battle.ally_health,
				'enemy_health': battle.enemy_health,
				'monsterhealth': battle.monster.health})
		else:
			return JsonResponse({
				'type': 'battleOngoing',
				'double': double,
				'skill': skillname,
				'health_used': health_used, 
				'damage': realdamage,
				'monster': battle.monster.name,
				'dialog': dialog,
				'ally_health': battle.ally_health,
				'enemy_health': battle.enemy_health,
				'monsterhealth': battle.monster.health})

@server_check
@login_required
@final_boss_check
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
			message = Message.objects.all().order_by('?')[0]
			return render(request, 'rpg/bossbattle.html',
					{'bossbattlemanager': bossbattlemanager,
						'bossbattle': mybossbattle,
						'character': character,
						'characters': characters,
						'percentage': percentage,
						'message': message.text})

		elif bossbattlemanager.state == "waiting":
			return render(request, 'rpg/getready.html',
					{'bossbattle': mybossbattle,
						'bossbattlemanager': bossbattlemanager})

		else:
			map = Map.objects.filter(is_open=True).order_by("-id")[0]
			bossmonster = Bossmonster.objects.get(map=map)
			bossbattlemanager = Bossbattlemanager.objects.create(group=character.group, bossmonster=bossmonster)
			codes = RegistrationCode.objects.filter(group=character.group)
			bossbattlemanager.enemy_health = bossmonster.health * len(codes)
			bossbattlemanager.save()
			return render(request, 'rpg/getready.html',
					{'bossbattle': mybossbattle,
						'bossbattlemanager': bossbattlemanager})


	elif request.method == 'POST':
		characters = Character.objects.filter(group=character.group)
		threshold = timezone.now() - datetime.timedelta(seconds=5)
		bossbattles = Bossbattle.objects.filter(character__in=characters, ready_time__gt=threshold)

		if request.POST.get("type", False) == 'ready':
			mybossbattle.ready = True
			mybossbattle.save()

			return JsonResponse({
				'numOfReady': len(bossbattles.filter(ready=True)),
				'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'unready':
			mybossbattle.ready = False
			mybossbattle.save()
			return JsonResponse({
				'numOfReady': len(bossbattles.filter(ready=True)),
				'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'refresh':
			mybossbattle.ready_time = timezone.now()
			mybossbattle.save()
			
			if len(bossbattles) == len(bossbattles.filter(ready=True)) and len(bossbattles) != 0 and (len(bossbattles) >= 5 or request.user.is_staff):
				bossbattlemanager.state = "ready"
				bossbattlemanager.boss_type = random.choice(["math", "phys", "chem", "life", "prog"])
				bossbattlemanager.start_time = timezone.now()
				bossbattlemanager.save()
			
			return JsonResponse({
				'numOfReady': len(bossbattles.filter(ready=True)),
				'numOfGroup': len(bossbattles)})

		elif request.POST.get("type", False) == 'attack':

			if request.POST.get("turn", False) == unicode(bossbattlemanager.turn):

				skill = get_skill(character, request.POST.get("skill", False))

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
				return JsonResponse({
					"type": bossbattlemanager.state,
					"givenskill": bossbattlemanager.bossmonster.skill.name,
					"normalskill1": bossbattlemanager.skill1.name,
					"normalskill2": bossbattlemanager.skill2.name,
					"monster": bossbattlemanager.bossmonster.name,
					"turn": bossbattlemanager.turn,
					"enemy_health": bossbattlemanager.enemy_health})

			if request.POST.get("turn", False) == unicode(bossbattlemanager.turn):
				if bossbattlemanager.start_time + datetime.timedelta(seconds=15) < timezone.now():
					bossbattlemanager.start_time = timezone.now()
					bossbattlemanager.save()

					dialognum = random.randrange(0, 10)
					bossbattlemanager.dialognum = dialognum

					characters = Character.objects.filter(group=character.group)
					bossbattles = Bossbattle.objects.filter(character__in=characters)

					calculate_boss_damage(bossbattles, bossbattlemanager)
	
					if bossbattlemanager.enemy_health <= 0:

						give_boss_skills(character.group, bossbattlemanager.bossmonster.skill)

						normalskills = Skill.objects.filter(math=False, phys=False, chem=False, life=False, prog=False, boss=False)
						combinations = Combination.objects.all()
						skillsWithComb = set([combination.new_skill for combination in combinations])
						normSkillsWithoutComb = list(set(normalskills) - skillsWithComb)

						skill1 = random.choice(normSkillsWithoutComb)
						skill2 = random.choice(normSkillsWithoutComb)

						give_boss_skills(character.group, skill1)
						give_boss_skills(character.group, skill2)

						bossbattlemanager.skill1 = skill1
						bossbattlemanager.skill2 = skill2
						bossbattlemanager.save()

						make_bossmonsterbook(bossbattlemanager)
						delete_bossbattles(bossbattlemanager, bossbattles, "win")

						return JsonResponse({
							"type": "win",
							"normalskill1": skill1.name,
							"normalskill2": skill2.name,
							"givenskill": bossbattlemanager.bossmonster.skill.name,
							"monster": bossbattlemanager.bossmonster.name,
							"turn": bossbattlemanager.turn,
							"enemy_health": bossbattlemanager.enemy_health})

					elif bossbattlemanager.turn + 1 >= 20:

						make_bossmonsterbook(bossbattlemanager)
						delete_bossbattles(bossbattlemanager, bossbattles, "lose")

						return JsonResponse({
							"type": "lose",
							"monster": bossbattlemanager.bossmonster.name,
							"turn": bossbattlemanager.turn,
							"enemy_health": bossbattlemanager.enemy_health})

					bossskill = boss_attack(bossbattlemanager, bossbattles)

					bossbattlemanager.bossskill = bossskill
					bossbattlemanager.turn += 1
					bossbattlemanager.save()

			codes = RegistrationCode.objects.filter(group=character.group)
			monsterhealth = len(codes) * bossbattlemanager.bossmonster.health

			mybossbattle = Bossbattle.objects.get(character=character)

			bossmonster = bossbattlemanager.bossmonster
			dialogs = [bossmonster.dialog1, bossmonster.dialog2, bossmonster.dialog3, bossmonster.dialog4, bossmonster.dialog5, bossmonster.dialog6, bossmonster.dialog7, bossmonster.dialog8, bossmonster.dialog9, bossmonster.dialog10]
			dialog = dialogs[bossbattlemanager.dialognum]

			return JsonResponse({
				"type": "everyonesecond",
				"bossskill": bossbattlemanager.bossskill,
				"bosstype": bossbattlemanager.boss_type,
				"bossdamage": bossbattlemanager.bossmonster.damage,
				"bannedtype": bossbattlemanager.banned_type,
				"monster": bossbattlemanager.bossmonster.name,
				"turn": bossbattlemanager.turn,
				"ally_health": mybossbattle.ally_health,
				"enemy_health": bossbattlemanager.enemy_health,
				"monsterhealth": monsterhealth,
				"dialog": dialog})

@server_check
@login_required
@final_boss_check
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
@final_boss_check
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
@final_boss_check
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
@final_boss_check
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
				if have.number == 0 and not have.skill.boss:
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

@login_required
def reward(request):
	if not request.user.is_staff:
		return redirect('index')

	grouplist = Group.objects.all()
	bossbattlemanagers = Bossbattlemanager.objects.all()
	characters = Character.objects.all()
	skillbooks = Skillbook.objects.all()
	groupbossgrades = []
	groupmonstergrades = []
	groupfailedCombicounts = []
	groupbossbattles = []
	groupcustoms = []

	for group in grouplist:
		bossmonsterbooks = Bossmonsterbook.objects.filter(group = group)
		bossgrades = [bossmonsterbook.grade.name for bossmonsterbook in bossmonsterbooks]
		bossgrade = 0
		for grade in bossgrades:
			if grade == 'A':
				bossgrade += 4
			elif grade == 'B':
				bossgrade += 3
			elif grade == 'C':
				bossgrade += 2
			elif grade == 'D':
				bossgrade += 1
		if len(bossgrades) != 0:
			bossgrade /= float(len(bossgrades))
		else:
			bossgrade = 0

		groupbossgrades += [[group.group_name, bossgrade,  bossgrades]]
		monsterbooks = Monsterbook.objects.filter(group = group)
		monstergrades = [monsterbook.grade.name for monsterbook in monsterbooks]
		Acount = monstergrades.count('A')
		Bcount = monstergrades.count('B')
		Ccount = monstergrades.count('C')
		Dcount = monstergrades.count('D')
		Fcount = monstergrades.count('F')
		normalgrade = (4 * Acount + 3 * Bcount + 2 * Ccount + 1 * Dcount)/float(Acount + Bcount + Ccount + Dcount + Fcount)
		groupmonstergrades += [[group.group_name, normalgrade, Acount, Bcount, Ccount, Dcount, Fcount]]
		failedCombinations = FailedCombination.objects.filter(group = group)
		groupfailedCombicounts += [[group.group_name, len(failedCombinations)]]
		bossbattlemanagers = Bossbattlemanager.objects.filter(Q(group = group)&(Q(state = 'win') | Q(state = 'lose')))
		groupbossbattles += [[group.group_name, len(bossbattlemanagers)]]
		clothescount = len(Clotheshave.objects.filter(Q(group = group)&Q(clothes__is_event=0)))
		eyecount = len(Eyehave.objects.filter(Q(group=group)&Q(eye__is_event=0)))
		haircount = len(Hairhave.objects.filter(Q(group=group)&Q(hair__is_event=0)))
		groupcustoms += [[group.group_name, clothescount+eyecount+haircount, clothescount, eyecount, haircount]]
	
	groupbossgrades.sort(key=lambda x: -x[1])
	groupmonstergrades.sort(key=lambda x: -x[1])
	groupbossbattles.sort(key=lambda x: -x[1])	
	groupfailedCombicounts.sort(key=lambda x: -x[1])
	groupbossbattles.sort(key=lambda x: -x[1])
	groupcustoms.sort(key=lambda x: -x[1])

	characterstats = {}
	monsterfinders = []
	monsterchampions = []
	skillfinders = []

	for idx, character in enumerate(characters):
		stat = character.math+character.phys+character.chem+character.life+character.prog
		characterstats[character.user.last_name+character.user.first_name]=stat
		monsterfinders += [[character.user.last_name+character.user.first_name+'('+character.group.group_name+')', len(Monsterbook.objects.filter(finder=character))]]
		monsterchampions += [[character.user.last_name+character.user.first_name+'('+character.group.group_name+')', len(Monsterbook.objects.filter(champion=character))]]
		skillfinders += [[character.user.last_name+character.user.first_name+'('+character.group.group_name+')', len(Skillbook.objects.filter(finder=character))]]

	monsterfinders.sort(key=lambda x: -x[1])
	monsterchampions.sort(key=lambda x: -x[1])
	skillfinders.sort(key=lambda x: -x[1])

	characterstats = sorted(characterstats.items(), key=lambda t : t[1], reverse=True)

	monsterfinders = monsterfinders[0:10]
	monsterchampions = monsterchampions[0:10]
	skillfinders = skillfinders[0:10]
	characterstats = characterstats

	groupkills = [[group.group_name, group.kill] for group in grouplist]
	groupkills.sort(key=lambda x: -x[1])

	
	
	return render(request, 'rpg/reward.html', { 'groupbossgrades': groupbossgrades, 'groupmonstergrades': groupmonstergrades, 'groupfailedCombicounts': groupfailedCombicounts, 'groupbossbattles': groupbossbattles, 'characterstats': characterstats, 'monsterfinders': monsterfinders, 'monsterchampions': monsterchampions, 'skillfinders': skillfinders, 'groupkills': groupkills, 'groupcustoms': groupcustoms, })
