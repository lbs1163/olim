# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0005_auto_20180108_0749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monster',
            old_name='exp',
            new_name='chem_exp',
        ),
        migrations.RemoveField(
            model_name='monster',
            name='type',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='type',
        ),
        migrations.AddField(
            model_name='monster',
            name='life_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monster',
            name='math_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monster',
            name='phys_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monster',
            name='prog_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='chem',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='life',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='math',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='phys',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='prog',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]