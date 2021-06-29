from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('teamprofile/', views.team_profile, name='teamprofile'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.team_update, name='update'),
    path('add/', views.add_member, name='add'),
    path('remove/<int:id>/', views.remove_member, name='remove'),
    path('change/', views.change_password, name='change'),
    path('login_phone/', views.login_phone, name='loginphone'),
    path('verify/', views.verify, name='verify'),

]
