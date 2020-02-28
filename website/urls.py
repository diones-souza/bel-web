from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index, name='index'),
    path('ajax',views.Ajax, name='ajax'),
    path('insert', views.Insert, name='insert'),
    path('list', views.List, name='list'),
    path('edit', views.Edit, name='edit'),
    path('remove',views.Remove, name='remove'),
]