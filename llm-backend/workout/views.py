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

    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ModifyWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        # Update the workout inputs
        try:
            workout = Workout.objects.get(pk=id)
        except Workout.DoesNotExist:
            return Response({'error': 'Workout not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkoutSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_CREATED)