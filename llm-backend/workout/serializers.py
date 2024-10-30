from rest_framework import serializers
from workout.models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'id', 
            'user',
            'created',
            'length',
            'difficulty',
            'workout_type',
            'target_area',
            'equipment_access',
            'included_exercises',
            'excluded_exercises',
            'other_considerations',
            'llm_suggested_changes',
            'llm_suggested_workout',
            'llm_final_workout',
            'workout_rating',
            'workout_comments'
        ]
        read_only_fields = ['id', 'user', 'created']
    