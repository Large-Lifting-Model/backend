from rest_framework import serializers

#Local imports
from .models import LLMPrompt

class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMPrompt
        fields = ['id', 'prompt_text', 'response_text']

