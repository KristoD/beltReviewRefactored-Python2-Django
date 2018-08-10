from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'new$', views.new_book),
    url(r'process/(?P<action>\w+)$', views.process),
    url(r'review/destroy/(?P<id>\d+)$', views.destroy),
    url(r'show/(?P<id>\d+)$', views.show),
]