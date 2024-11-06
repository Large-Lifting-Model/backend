from django.shortcuts import render
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

#For llm prompting
from backend.settings import API_KEY, MODEL_VERSION
from .prompts import prompt_start, prompt_end
import google.generativeai as genai


class CreateWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    '''Create Workout'''
    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                llm = LlmConnection()
                llm.requestWorkout(serializer)
            except:
                print("[ERROR]: LLM Request Failed")
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
        
    '''Delete Workout'''
    def delete(self, request, id):
        try:
            workout = Workout.objects.get(user=request.user, id=id)
            workout.delete()
            return Response({"message": "Workout deleted successfully."}, status=status.HTTP_200_OK)
        except Workout.DoesNotExist:
            return Response({"error": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        

''' Used to connect and query llm'''
class LlmConnection():

    api_key = API_KEY
    model_version = MODEL_VERSION
    model = genai.GenerativeModel(model_version)

    def __init__(self):
        genai.configure(api_key = self.api_key)
        return

    '''Request a workout from the llm'''
    def requestWorkout(self, serializer):
        print("[INFO]: Connecting to Gemini")
        prompt = self.generatePrompt(serializer.validated_data)
        response = self.model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text
    
    '''Make changes to the current llm workout'''
    def changeWorkout(self, serializer):
        prompt = self.generatePrompt(serializer.validated_data)
        return
    
    '''Generates llm prompts'''
    def generatePrompt(self, serial_val_data):
        print("[INFO]: Creating Prompt")
        prompt = prompt_start
        for field in Workout._meta.get_fields():
            name = field.name
            val = serial_val_data.get(name)
            prompt += str(name) + ": " + str(val) + "\n"
        prompt += prompt_end
        return prompt


