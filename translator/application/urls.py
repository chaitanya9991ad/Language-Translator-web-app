from django.urls import path
from . import views

urlpatterns = [
    path('api/users/register/', views.register_user),
    path('api/users/login/', views.login_user),
    path('api/users/detail/', views.user_detail),
    path('api/translate/', views.translate_text),
    path('', views.frontend), 
]