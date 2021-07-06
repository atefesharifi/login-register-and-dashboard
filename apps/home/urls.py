from django.urls import path
from . import views

app_name= 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('sendcode/', views.sendcode, name='sendcode'),
]
