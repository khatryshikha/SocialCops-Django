from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name ='home'),
    url(r'^upload', views.check_new_entry, name ='upload'),
    url(r'^stop', views.stop_csv, name ='stop'),
    url(r'^export_details', views.export_details, name ='export_details'),
    url(r'^export', views.get_csv_export, name ='export'),
]