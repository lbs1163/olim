# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-08 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0007_auto_20180108_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='character',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rpg.Character'),
        ),
    ]
