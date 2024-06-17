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
from .views import FighterDetailView, FightHighlightListView, aktualnosci, add_article, article_list, fighters, add_event, event_list, event_detail, ArticleDeleteView, article_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('aktualnosci/', aktualnosci, name='aktualnosci'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete_article'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('add_article/', add_article, name='add_article'),
    path('article_list/', article_list, name='article_list'),
    path('add_event/', add_event, name='add_event'),
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('organizacje/', views.organizacje, name='organizacje'),
    path('user_login/', views.login_view, name='user_login'),
    path('register/', views.register_view, name='register'),
    path('user_logout/', views.logout_view, name='user_logout'),
    path('create_fighter/', views.create_fighter, name='create_fighter'),
    path('add_fighter/', views.add_fighter, name='add_fighter'),
    path('fighters/', fighters, name='fighters'),
    path('fighter/<int:pk>/', FighterDetailView.as_view(), name='fighter-detail'),
    path('highlights/', views.FightHighlightListView.as_view(), name='fight_highlights_list'),
    path('skroty_walk/', FightHighlightListView.as_view(), name='fight_highlights_list'),
    path('bet/<int:fight_id>/', views.bet_on_fight, name='bet_on_fight'),
    path('bet_ranking/', views.bet_ranking, name='bet_ranking'),
    path('article/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('fighters/search/', views.search_fighters, name='fighter_search'),
    path('fighters/<int:fighter_id>/', views.fighter_detail, name='fighter_detail'),

]