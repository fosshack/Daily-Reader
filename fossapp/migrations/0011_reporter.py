# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fossapp', '0010_auto_20170419_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fossapp.UserProfile')),
            ],
        ),
    ]
