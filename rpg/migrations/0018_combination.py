# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-14 04:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0017_auto_20180113_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_skill', to='rpg.Skill')),
                ('skill01', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill01', to='rpg.Skill')),
                ('skill02', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill02', to='rpg.Skill')),
            ],
        ),
    ]
