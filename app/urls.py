from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name ='home'),
    url(r'^upload', views.check_new_entry, name ='upload'),
    url(r'^stop', views.stop_csv, name ='stop'),
]