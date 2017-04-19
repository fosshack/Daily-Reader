from . import views
from django.conf.urls import url
from . import api_views

app_name='fossapp'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/$', views.home),
    url(r'^category/(?P<id>[0-9]+)/$', views.category),
    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),
    url(r'^views/$', views.views_count),
    url(r'^dash/$', views.dashboard),
    url(r'^getnews/$', views.getnews),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.user_login, name='signin'),
    url(r'^signout/$', views.user_logout, name='signout'),
    url(r'^news/(?P<pk>[0-9]+)$', api_views.news_detail),
    url(r'^feed/$', views.newsfeed),
]