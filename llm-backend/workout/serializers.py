from rest_framework import serializers
from workout.models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 
                  'created', 
                  'length', 
                  'difficulty',
                  'workout_type', 
                  'target_area',
                  'equipment_access', 
                  'included_exercises', 
                  'excluded_exercises',
                  'other_considerations'
                  # placeholder for LLM attribute
                  ]