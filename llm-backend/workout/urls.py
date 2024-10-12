from django.urls import path
from . import views

urlpatterns = [
    path('CreateWorkout/', views.CreateWorkoutView.as_view())
]