from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    re_path(r'^processo/(?P<cod>\d{4}\.\d{3}\.\d{6}-\d)/(?P<index>\d+)/$', views.process_view, name='processo')
   
]