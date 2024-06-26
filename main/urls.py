from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_solutions/', views.get_solutions, name='get_solutions'),
    path('get_form/', views.get_form, name='get_form'),
    path('get_activity_detail/', views.get_activity_detail, name='get_activity_detail'),
    path('get_free_economic_zones_by_emirate_name/', views.get_free_economic_zones_by_emirate_name, name='get_free_economic_zones_by_emirate_name'),
]
