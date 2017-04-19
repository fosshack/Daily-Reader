from .models import *
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=25)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'slug', 'is_reporter', 'upvoted', 'downvoted', 'interests', ]

    def clean_aadhar_no(self):
        aadhar_no = self.cleaned_data['aadhar_no']
        if not aadhar_no.isdigit():
            raise forms.ValidationError('Please enter a valid Aadhar number.')
        else:
            return aadhar_no

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if contact.isdigit() and len(contact) == 10:
            return contact
        else:
            raise forms.ValidationError('Please enter a valid 10 digit contact number.')


class NewsForm(ModelForm):
    content_short = forms.CharField(widget=forms.Textarea)
    content_long = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = News
        exclude = ['views','downvotes','upvotes','is_voted','average','publish_date','published_by']