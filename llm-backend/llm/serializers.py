from rest_framework import serializers
from llm.models import LLMModel

class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = ['workout_text']

