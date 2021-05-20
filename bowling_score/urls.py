from django.urls import path
from bowling_score import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game_view, name='game'),
]
