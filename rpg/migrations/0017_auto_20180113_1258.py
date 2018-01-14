# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-13 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0016_monster_health'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('is_open', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='monster',
            name='map',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Map'),
        ),
    ]