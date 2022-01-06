from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login_view, name='login_view'),
    path('api/dashboard/', views.dashboard_view, name='dashboard_view'),
    path('api/edit/', views.edit_view, name='edit_view'),
    path('api/delete/', views.delete_view, name='delete_view'),
    path('api/logout/', views.logout_view, name='logout_view'),
]
