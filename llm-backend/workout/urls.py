from django.urls import path
from . import views

urlpatterns = [
    path('createworkout/', views.CreateWorkoutView.as_view(), name='create-workout'),
    path('viewworkouts/', views.WorkoutView.as_view(), name='workout-list')
]