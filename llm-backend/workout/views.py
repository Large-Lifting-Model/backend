from django.shortcuts import render
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Will need to associate this with users
class CreateWorkoutView(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    # permission_classes = [IsAuthenticated]