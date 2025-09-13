from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chat/', views.get_gemini_response, name='get_gemini_response'),
]
