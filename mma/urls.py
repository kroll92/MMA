"""
URL configuration for mma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from . import views
from .views import FighterDetailView, FightHighlightListView, aktualnosci, article_detail, add_article, article_list, fighters

urlpatterns = [
    path('', views.index, name='index'),
    path('aktualnosci/', aktualnosci, name='aktualnosci'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('add_article/', add_article, name='add_article'),
    path('article_list/', article_list, name='article_list'),
    path('events/', views.events, name='events'),
    path('organizacje/', views.organizacje, name='organizacje'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add_event/', views.add_event, name='add_event'),
    path('create_fighter/', views.create_fighter, name='create_fighter'),
    path('add_fighter/', views.add_fighter, name='add_fighter'),
    path('fighters/', fighters, name='fighters'),
    path('fighter/<int:pk>/', FighterDetailView.as_view(), name='fighter-detail'),
    path('highlights/', views.FightHighlightListView.as_view(), name='fight_highlights_list'),
    path('skroty_walk/', FightHighlightListView.as_view(), name='fight_highlights_list'),
]