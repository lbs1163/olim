# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-01 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0009_merge_20180129_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalbossbattle',
            name='turn',
        ),
        migrations.RemoveField(
            model_name='finalbossbattlemanager',
            name='turn',
        ),
        migrations.AddField(
            model_name='finalbossbattle',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]
