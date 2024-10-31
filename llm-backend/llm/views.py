from django.shortcuts import render
from rest_framework.views import APIView
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework import status
from backend.settings import API_KEY, MODEL_VERSION


#Local imports
from .models import LlmPrompt
from .serializers import LlmSerializer

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
        genai.configure(api_key= API_KEY)
        model = genai.GenerativeModel(MODEL_VERSION)
        response = model.generate_content(text)
        return response.candidates[0].content.parts
    
    def createPrompt(self):
        workout_text_outline = "Workout Parameters:\n"

        #Adjust for correct model
        for field in LlmPrompt._meta.get_fields():
            name = field.name
            val = getattr(LlmPrompt.objects.last(), name)
            workout_text_outline += str(name) + ": " + str(val) + "\n"

        #Add routine for personal parameters
        ######



        ######
        print(workout_text_outline)
        return workout_text_outline
    
    def get(self, request, format = None):
        model_data = LlmPrompt.objects.all()
        serializer = LlmSerializer(model_data, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = LlmSerializer(data = request.data)
        #Change var as needed
        prompt_text = self.createPrompt()
        if serializer.is_valid():
            text = serializer.validated_data.get('prompt_text')
            #serializer.save(response_text = self.askLlm(text))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



