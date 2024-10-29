from django.shortcuts import render
from rest_framework.views import APIView
import google.generativeai as genai
from ..backend.settings import API_KEY, MODEL_VERSION
from llm.models import LLMModel, LLMPrompt
from django.http import Http404
from rest_framework.response import Response

def index(request):
    return render(request, 'llm/')

class LLMView(APIView):
    
    def 

#####################
#### FOR TESTING ####
class LLMPrompt(APIView):

    def get(self, request):
        prompt = self
        



# Example prompt
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)