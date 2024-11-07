from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, HealthData

class HealthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthData
        fields = [
            'dob', 
            'gender', 
            'height', 
            'weight', 
            'favourite_workout_type', 
            'workout_experience', 
            'fitness_goal', 
            'injuries', 
            'other_considerations',
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    # Include fields from the User model
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    is_new = serializers.BooleanField(read_only=True) 

    health_data = HealthDataSerializer()

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'is_new', 'health_data']
        read_only_fields = ['email']  # Make email read only

    def update(self, instance, validated_data):
        # Update user fields (first_name, last_name, email)
        user_data = validated_data.pop('user', {})
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')


        # Disable email update for now
        # email = user_data.get('email')
        
        if first_name:
            instance.user.first_name = first_name
        if last_name:
            instance.user.last_name = last_name
        # if email:
        #     instance.user.email = email
        instance.user.save()

        # Update health data fields
        health_data = validated_data.pop('health_data', {})
        health_data_instance = instance.health_data
        for attr, value in health_data.items():
            setattr(health_data_instance, attr, value)
        health_data_instance.save()

        # Update other profile fields if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance