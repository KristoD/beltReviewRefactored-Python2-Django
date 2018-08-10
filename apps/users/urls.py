from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.show)
]