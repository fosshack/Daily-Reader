# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 00:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fossapp', '0008_auto_20170419_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(related_name='category', to='fossapp.Category'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]