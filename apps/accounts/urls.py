from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/<int:pk>/', views.OTPLogin.as_view(), name='second_login'),
    path('register/', views.register, name='register'),
    path('teamprofile/', views.team_profile, name='teamprofile'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.team_update, name='update'),
    path('add/', views.add_member, name='add'),
    path('remove/<int:id>/', views.remove_member, name='remove'),
    path('addadmin/', views.update_admin, name='add_admin'),
    path('duplicate/<int:pk>/', views.pass_duplicate, name='duplicate'),

]
