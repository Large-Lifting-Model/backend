from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name=''),
    path('prompts/', views.LLMPrompt.as_view())
]
