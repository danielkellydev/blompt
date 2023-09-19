from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_ai_assistance/', views.get_ai_assistance, name='get_ai_assistance'),  # Moved this inside urlpatterns
]


