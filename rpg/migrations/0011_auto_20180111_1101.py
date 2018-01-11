# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0010_monsterbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='chem',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='life',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='math',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='phys',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='prog',
            field=models.IntegerField(default=0),
        ),
    ]
