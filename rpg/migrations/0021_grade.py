# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0020_server'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('turn', models.IntegerField(default=1)),
            ],
        ),
    ]