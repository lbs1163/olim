# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-09 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0012_auto_20180209_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
                ('clothes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Clothes')),
                ('eye', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Eye')),
                ('hair', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpg.Hair')),
            ],
        ),
    ]
