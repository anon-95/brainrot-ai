from django.urls import path
from .views import chat_view
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
]
