from rest_framework import serializers
from workout.models import Workout

# Will need to associate this with users
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 
                  'created', 
                  'length', 
                  'difficulty',
                  'workout_type', 
                  'target_area',
                  'included_exercises', 
                  'excluded_exercises',
                  'equipment_access', 
                  'other_considerations'
                  ]