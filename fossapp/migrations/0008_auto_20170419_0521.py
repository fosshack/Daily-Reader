# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fossapp', '0007_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='downvoted',
            field=models.ManyToManyField(related_name='downvoted', to='fossapp.News'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='upvoted',
            field=models.ManyToManyField(related_name='upvoted', to='fossapp.News'),
        ),
    ]
