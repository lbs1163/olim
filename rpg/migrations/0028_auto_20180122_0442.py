# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 04:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0027_auto_20180122_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bossbattle',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Skill'),
        ),
    ]
