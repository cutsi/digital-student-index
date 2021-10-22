from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name = "kino-home"),
    path('login', views.login, name = "users-login"),
]