# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0011_auto_20180111_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpg.Character')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpg.Skill')),
            ],
        ),
    ]