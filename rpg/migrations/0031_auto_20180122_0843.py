# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0030_auto_20180122_0505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bossbattle',
            name='skill',
        ),
        migrations.AddField(
            model_name='bossbattle',
            name='damage',
            field=models.IntegerField(default=0),
        ),
    ]