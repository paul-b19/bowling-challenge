from django.urls import path
from bowling_score import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]
