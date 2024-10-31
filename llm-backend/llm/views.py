from django.shortcuts import render
from rest_framework.views import APIView
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework import status
from backend.settings import API_KEY, MODEL_VERSION


#Local imports
from .models import LlmPrompt
from .serializers import LlmSerializer
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from users.models import HealthData 

# def index(request):
#     return render(request, 'llm/')

# def createLlmPrompt():
#     user_keys = [
#                  "Gender",
#                  "Height",
#                  "Weight",
#                  "Favourite Workout Type",
#                  "Workout Experince",
#                  "Fitness Goals",
#                  "Injuries"
#                  ]
    
#     workout_keys = [
#                  "Duration",
#                  "Difficulty",
#                  "Workout Style",
#                  "Targeted Areas",
#                  "Available Equipment",
#                  "Included Exercises",
#                  "Excluded Exercises",
#                  "Other Considerations"
#                  ]
    

#####################
#### FOR TESTING ####


 


class LlmPromptView(APIView):

    def askLlm(self, text):
        print("[INFO]: Getting Google Gemini Response")
        genai.configure(api_key= API_KEY)
        model = genai.GenerativeModel(MODEL_VERSION)
        response = model.generate_content(text)
        print("[INFO]: Returned LLM Response:\n")
        print("#################################")
        print(response.candidates[0].content.parts[0].text)
        print("#################################")

        return response.candidates[0].content.parts[0].text
    
    def createPrompt(self, ser_obj_data):
        print("[INFO]: Creating Prompt")
        workout_text_outline = "Create a workout with the following parameters. Only include the workout and the workout details.\nWorkout Parameters:\n"
        #Adjust for correct model
        for field in Workout._meta.get_fields():
            name = field.name
            #val = getattr(Workout.objects.last(), name)
            val = ser_obj_data.get(name)
            workout_text_outline += str(name) + ": " + str(val) + "\n"

        # workout_text_outline += "Health Parameters:\n"
        # for field in HealthData._meta.get_fields():
        #     name = field.name
        #     val = getattr(HealthData.objects.last(), name)
        #     workout_text_outline += str(name) + ": " + str(val) + "\n"
        workout_text_outline += "\nReturn your response in pure text format using only new line delimiters with no markdown styling."
        return workout_text_outline
    
    def get(self, request, format = None):
        model_data = Workout.objects.all()
        serializer = WorkoutSerializer(model_data, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = WorkoutSerializer(data = request.data)
        if serializer.is_valid():
            prompt_text = self.createPrompt(serializer.validated_data)
            response_text = self.askLlm(prompt_text)
            serializer.save(llm_final_workout = response_text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



