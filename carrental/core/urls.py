from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stores', views.storelist, name='storelist'),
]