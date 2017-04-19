from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.forms import forms, ModelForm
from datetime import datetime, timedelta
from django.template.defaultfilters import slugify


# Create your models here.


class UserProfile(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    is_reporter = models.BooleanField(default=False)
    aadhar_no = models.CharField(max_length=12, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    sex = models.CharField(choices=SEX_CHOICES, blank=False, max_length=1)
    location = models.CharField(max_length=100, blank=False)
    slug = models.SlugField()
    dp = models.ImageField(blank=True)
    upvoted = models.ManyToManyField('News', related_name='upvoted', blank=True, null=True)
    downvoted = models.ManyToManyField('News', related_name='downvoted', blank=True, null=True)
    interests = models.ManyToManyField('Category', related_name='category', blank=True, null=True)

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.first_name + ' ' + self.user.last_name)
        super().save(*args, **kwargs)


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Reporter(models.Model):
    reporter = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.reporter.user.username


class News(models.Model):
    category = models.ForeignKey(Category)
    news_title = models.CharField(max_length=100)
    location = models.CharField(max_length=50, default='kalady')
    publish_date = models.DateTimeField()
    content_short = models.CharField(max_length=300)
    content_long = models.CharField(max_length=2000)
    published_by = models.ForeignKey(UserProfile)
    tags = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    average = models.FloatField(default=0.0)
    is_voted = models.BooleanField(default=False)
    image = models.ImageField(default="")

    def __str__(self):
        return '%s %s %s' % (self.category.category_name, self.news_title, format(self.publish_date))


class Pinned_News(models.Model):
    news1 = models.ForeignKey(News)

    def __str__(self):
        return format(self.news1)


"""
user = request.user
usp = user.user_profile
usp.upvoted.add(post)
usp.save()
"""
