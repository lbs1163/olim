# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-10 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0014_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='bossmonster',
            name='dialog1',
            field=models.CharField(default='dialog1', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog10',
            field=models.CharField(default='dialog10', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog2',
            field=models.CharField(default='dialog2', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog3',
            field=models.CharField(default='dialog3', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog4',
            field=models.CharField(default='dialog4', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog5',
            field=models.CharField(default='dialog5', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog6',
            field=models.CharField(default='dialog6', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog7',
            field=models.CharField(default='dialog7', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog8',
            field=models.CharField(default='dialog8', max_length=50),
        ),
        migrations.AddField(
            model_name='bossmonster',
            name='dialog9',
            field=models.CharField(default='dialog9', max_length=50),
        ),
    ]
