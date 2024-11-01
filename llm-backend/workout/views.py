from django.shortcuts import render
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

class CreateWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    '''Create Workout'''
    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkoutListView(APIView):
    permission_classes = [IsAuthenticated]

    '''View workout history by user'''
    def get(self, request):
        workouts = Workout.objects.filter(user=request.user)
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    '''View workout'''
    def get(self, request, id):
        try:
            workout = Workout.objects.get(user=request.user, id=id)
            serializer = WorkoutSerializer(workout)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Workout.DoesNotExist:
            return Response({"error": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        
    '''Modify Workout'''
    def put(self, request, id):
        try:
            workout = Workout.objects.get(user=request.user, id=id)
            serializer = WorkoutSerializer(workout, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Workout.DoesNotExist:
            return Response({"error": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)