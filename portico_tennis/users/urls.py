from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('registration-pending/', TemplateView.as_view(template_name='users/registration_pending.html'), name='registration_pending'),

]
