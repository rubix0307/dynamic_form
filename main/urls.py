from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_form/', views.get_form, name='get_form'),
    path('search_activity/', views.search_activity, name='search_activity'),
    path('get_activity_detail/', views.get_activity_detail, name='get_activity_detail'),
]
