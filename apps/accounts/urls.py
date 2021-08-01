from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/<int:pk>/', views.OTPLogin.as_view(), name='second_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('duplicate/<int:pk>/', views.pass_duplicate, name='duplicate'),

]
