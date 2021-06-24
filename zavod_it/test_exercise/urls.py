from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("statistics", views.statistics, name="statistics"),
    path("add_news", views.add_news, name="add_news"),
    path("news/<int:id>", views.news, name="news")
]
