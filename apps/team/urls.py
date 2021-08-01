from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'team'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('get_content/', views.get_content, name='get_content'),
    path('frequently_question/', views.frequently_question, name='frequently_question'),
    path('profile/', views.team_update, name='team_profile'),
    path('result/', views.result, name='result'),
    path('sent_code/', views.sent_code, name='sent_code'),
    path('add/', views.add_member, name='add_member'),
    path('get_members/', views.get_members, name='get_members'),
    path('user/<pk>/delete', views.remove_member, name='remove'),
    path('user/<pk>', views.get_member, name='get_member'),
    path('user/<pk>/edit', views.team_user_update, name='update_member'),
    path('sendcode/', views.send_code, name='send_code'),

]
