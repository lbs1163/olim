# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-13 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0015_auto_20180113_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='health',
            field=models.IntegerField(default=0),
        ),
    ]