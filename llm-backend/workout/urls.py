from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateWorkoutView.as_view(), name='main-workout'),
    path('list/', views.WorkoutListView.as_view(), name='workout-list'),
    path('<int:id>/', views.WorkoutView.as_view(), name='specific-workout')
]