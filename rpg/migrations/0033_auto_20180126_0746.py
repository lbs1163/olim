# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0032_auto_20180122_0846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bossbattle',
            name='damage',
        ),
        migrations.RemoveField(
            model_name='bossbattlemanager',
            name='redo',
        ),
        migrations.AddField(
            model_name='bossbattle',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Skill'),
        ),
        migrations.AddField(
            model_name='bossbattle',
            name='turn',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bossbattlemanager',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
