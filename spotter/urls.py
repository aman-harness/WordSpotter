from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^submit/', views.receive),
    url(r'^show/', views.redir),
    # url(r'^(?P<word_id>\d+)/$', views.show_words)
    # url(r'^(?P<word_id>\d+)/$', views.show_words)
]