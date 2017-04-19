from django.shortcuts import render, get_object_or_404
from django.http import *
from itertools import chain
from django.db.models import Max
from django.template.loader import get_template
from django.template import Context
from .models import *
from .forms import *
from datetime import datetime, date
from django.apps import *
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
import random, traceback, json
from django.utils.safestring import mark_safe
from collections import Counter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core import serializers
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    print('Hellow')
    return HttpResponseRedirect('/home/')


def find_rate():
    news = News.objects.all()
    for news in news:
        news.average = news.upvotes / (news.upvotes + news.downvotes)
        news.save()
    return


def home(request):
    find_rate()
    date = datetime.now()
    olddate = date - timedelta(days=7)
    print(olddate)
    category = Category.objects.all()

    sports = News.objects.filter(category__id=1).order_by('-views')[:3]
    business = News.objects.filter(category__id=2).order_by('-views')[:3]
    international = News.objects.filter(category__id=3).order_by('-views')[:3]
    technology = News.objects.filter(category__id=5).order_by('-views')[:3]
    entertainment = News.objects.filter(category__id=4).order_by('-views')[:3]
    top_news = sorted(chain(sports, business,international,technology,),key=lambda instance: instance.publish_date,reverse=True)[:5]


    just_in = News.objects.filter().order_by('-publish_date')[:5]
    top_rated = News.objects.latest('average')
    must_read = Pinned_News.objects.get(id=1)
    daily_news = News.objects.latest('publish_date')
    trending = News.objects.latest('views')

    myreporters()
    getrepoters = Reporter.objects.all().order_by('-rating', 'reporter')[:4]

    # print(trending)
    return render(request, 'Home.html',
                  {'category': category, 'top_rated': top_rated, 'must_read': must_read, 'daily_news': daily_news,
                   'trending': trending,
                   'just_in':just_in,
                   'top_news':top_news,
                   'reporters':getrepoters})


def myreporters():
    users = UserProfile.objects.filter(is_reporter=True)
    for user in users:
        news = News.objects.filter(published_by=user)
        total = 0
        for item in news:
            total = total + item.average
        if len(news):
            average = total/len(news)
        else:
            average = 0
        try:
            reporter = Reporter.objects.get(reporter=user)
        except:
            reporter = Reporter()
        reporter.reporter = user
        reporter.rating = average
        reporter.save()


"""
def top_rated(request):
    toprated = News.objects.filter().order_by('-average')[:5]
    print(toprated.count())
    #print(toprated)
    return render(request, 'toprated.html', {'top_rated': toprated})


def must_read(request):
    must_read = Pinned_News.objects.all()
    return render(request, 'mustread.html', {'must_read': must_read})


def daily_news(request):
    daily_news = News.objects.filter().order_by('-date', '-average')[:5]
    return render(request, 'dailynews.html', {'daily_news': daily_news})


def trending(request):
    trending = News.objects.filter(publish_date__range=(olddate, date)).order_by('-average')[:5]
    return render(request, 'trending.html', {'trending': trending})
"""

def getCategory(id):
    cat = Category.objects.get(id=id)
    return cat


def category(request, id):
    date = datetime.now()
    olddate = date - timedelta(days=7)
    current_cat = getCategory(id)
    print(current_cat)
    if format(current_cat) == 'Top Rated':
        news = News.objects.filter().order_by('-average')[:5]
    elif format(current_cat) == 'Must Read':
        news = Pinned_News.objects.all()
    elif format(current_cat) == 'Daily News':
        news = News.objects.filter().order_by('-publish_date', '-average')[:5]
    elif format(current_cat) == 'Trending':
        news = News.objects.filter(publish_date__range=(olddate, date)).order_by('-average')[:5]
    else:
        news = News.objects.filter(category=current_cat).order_by('-publish_date')
    return render(request, 'category.html', {'current_cat': current_cat, 'news': news})


def views_count(request):
    id = request.POST.get("id")
    news = News.objects.get(id=id)
    news.views = news.views + 1
    news.save()
    # print("This is the viewd id = "+format(id))
    data = {'data': news.views}
    return JsonResponse(data)


def upvote(request):
    id = request.POST.get("id")
    user = request.user

    news = News.objects.get(id=id)
    if not news.is_voted:
        news.is_voted = True
        news.upvotes = news.upvotes + 1
        news.save()
    else:
        pass

    print("request reached in upvotes..id = " + format(id))
    data = {'data': news.upvotes}
    return JsonResponse(data)


def downvote(request):
    id = request.POST.get("id")
    news = News.objects.get(id=id)
    if not news.is_voted:
        news.is_voted =True
        news.downvotes = news.downvotes + 1
        news.save()
    else:
        pass
    # print("request reached in downvotes..id = " + format(id))
    data = {'data': news.downvotes}
    return JsonResponse(data)

@login_required
def dashboard(request):
    user = UserProfile.objects.get(user=request.user)
    if request.POST:
        formset = NewsForm(request.POST,request.FILES)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.publish_date=datetime.now()
            form.published_by=user
            form.save()
            return render(request, 'dashboard.html', {})
        else:
            print(formset.errors)

    else:
        print("error in outer else")     
    return render(request, 'dashboard.html', {})


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        userprofile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.save()
            user.set_password(user.password)
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            messages.success(request, "You've signed up successfully!")
            return HttpResponseRedirect('/signin/')
        else:
            return render(request, 'signup.html', {'user_form': user_form, 'userprofile_form': userprofile_form})
    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()
        return render(request, 'signup.html', {'user_form': user_form, 'userprofile_form': userprofile_form})


def user_login(request):
    invalid = True
    redirect_to = None
    if 'redirect' in request.GET:
        redirect_to = request.GET['redirect']
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            invalid = False
            if user.is_active:
                login(request, user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account has been deactivated.")
        else:
            messages.error(request, 'Invalid credentials supplied!')
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'login.html', {'invalid': invalid, }, )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'login.html', {})


def getnews(request):
    id = request.POST.get('id')
    print(id)
    news = News.objects.filter(id=id)
    data = serializers.serialize('json', news)
    return JsonResponse(data,safe=False)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/signin/')


def newsfeed(request):
    news = News.objects.all().order_by('-publish_date')
    paginator = Paginator(news, 4)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)
    if request.POST.get('mysubmitbtn'):
        print("inside post")
        tags = request.POST.get('mysearchname')
        news = News.objects.filter(tags__icontains=tags)
        paginator = Paginator(news, 4)  # Show 5 posts per page
        page = request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            news = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            news = paginator.page(paginator.num_pages)
            length = len(news)
        return render(request, 'newsfeed.html', {'news': news,'length':length})
    length = len(news)
    return render(request, 'newsfeed.html', {'news': news,'length':length})
