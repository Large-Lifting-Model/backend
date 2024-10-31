from django.shortcuts import render
from rest_framework.views import APIView
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework import status
from backend.settings import API_KEY, MODEL_VERSION


#Local imports
from .models import LLMPrompt as LLMModel
from .serializers import LLMSerializer

# def index(request):
#     return render(request, 'llm/')


#####################
#### FOR TESTING ####
class LLMPrompt(APIView):

    def askLLM(self, text):
        genai.configure(api_key= API_KEY)
        model = genai.GenerativeModel(MODEL_VERSION)
        response = model.generate_content(text)
        return response.candidates[0].content.parts

    def get(self, request, format = None):
        prompt = LLMModel.objects.all()
        serializer = LLMSerializer(prompt, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = LLMSerializer(data = request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('prompt_text')
            serializer.save(response_text = self.askLLM(text))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

