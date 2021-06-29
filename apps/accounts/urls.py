from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/<int:pk>/', views.OTPLogin.as_view(), name='second_login'),
    path('register/', views.register, name='register'),
    path('teamprofile/', views.team_profile, name='teamprofile'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update/', views.team_update, name='update'),
    path('add/', views.add_member, name='add'),
    path('remove/<int:id>/', views.remove_member, name='remove'),
    path('change/', views.change_password, name='change'),

]
