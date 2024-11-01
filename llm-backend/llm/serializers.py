from rest_framework import serializers

#Local imports
from .models import LlmPrompt

class LlmSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmPrompt
        fields = ['id', 'prompt_text', 'response_text']

