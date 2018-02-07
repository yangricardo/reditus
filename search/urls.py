from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    re_path(r'^processo/(?P<cod>[0-9]{4}\.[0-9]{3}\.[0-9]{6}-[0-9])/(?P<index>[0-9]+)/$', views.process_view, name='processo')
   
]