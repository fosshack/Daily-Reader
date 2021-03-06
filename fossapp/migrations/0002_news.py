# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 07:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fossapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=100)),
                ('publish_date', models.DateTimeField()),
                ('content_short', models.CharField(max_length=300)),
                ('content_long', models.CharField(max_length=2000)),
                ('tags', models.CharField(max_length=100)),
                ('views', models.IntegerField(default=0)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fossapp.Category')),
                ('published_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
