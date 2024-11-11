from rest_framework import serializers
from workout.models import Workout, Recommendation

class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)
    
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
            'other_workout_considerations',
            'llm_suggested_changes',
            'llm_suggested_workout',
            'llm_final_workout',
            'workout_rating',
            'workout_comments'
        ]
        read_only_fields = ['id', 'user', 'created']
    
class RecommendationSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Recommendation
        fields = [
            'id', 
            'user',
            'created',
            'recommendation'
        ]