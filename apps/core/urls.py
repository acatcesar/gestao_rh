from django.urls import path, include
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('user/<str:username>/', views.get_github_user_info, name='github_user_info'),
    path('user/', views.get_cotacao, name='get_cotacao'),

]