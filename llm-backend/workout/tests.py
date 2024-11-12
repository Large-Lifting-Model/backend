from django.test import TestCase
from rest_framework.test import APITestCase
from unittest.mock import Mock
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from users.models import HealthData
from users.serializers import UserProfileSerializer

User = get_user_model()

class CreateWorkoutTest(APITestCase):
    def setUp(self):
        # Create a test user to retrieve auth token
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        # self.health_data = HealthData.objects.update(
        #     profile_id=self.user.pk,  # Link health data to the profile
        #     dob='1990-01-01',
        #     gender='Male',
        #     height=1.75,
        #     weight=75,
        #     favourite_workout_type='Cardio',
        #     workout_experience='Intermediate',
        #     fitness_goal='Build muscle',
        #     injuries='None',
        #     other_considerations='None'
        # )
        
        # self.assertEqual(self.health_data.gender, 'Male')

        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
    
    def test_post_workout(self):
        # Check authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('create-workout')
        data = {
            'length': 60,
            'difficulty': 'Easy',
            'workout_type': 'Weights',
            'target_area': 'Chest',
            'equipment_access': 'Full Gym'
        }
        response = self.client.post(url, data, format='json')

        # Asset workout post is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['length'], 60)
        self.assertEqual(response.data['difficulty'], 'Easy')
        self.assertEqual(response.data['workout_type'], 'Weights')
        self.assertEqual(response.data['target_area'], 'Chest')
        self.assertEqual(response.data['equipment_access'], 'Full Gym')
        


# class WorkoutListTest(APITestCase):
#     def setUp(self):
#         # Create a test user to retrieve auth token
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword',
#             first_name='Test',
#             last_name='User'
#         )
#         self.refresh_token = RefreshToken.for_user(self.user)
#         self.access_token = str(self.refresh_token.access_token)
        
#         # Create a test workout
#         self.workout = Workout.objects.create(
#             length=60,
#             difficulty='Easy',
#             workout_type='Weights',
#             target_area='Chest',
#             equipment_access='Full Gym'
#         )
    
#     def test_get_workout_list(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('workout-list')
#         response = self.client.get(url)
#         serialized_data = WorkoutSerializer([self.workout], many=True).data

#         # Assert workout data is returned successfully
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serialized_data)

# class WorkoutViewTest(APITestCase):
#     def setUp(self):
#         # Create a test user to retrieve auth token
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword',
#             first_name='Test',
#             last_name='User'
#         )
#         self.refresh_token = RefreshToken.for_user(self.user)
#         self.access_token = str(self.refresh_token.access_token)
        
#         # Create a test workout
#         self.workout = Workout.objects.create(
#             length=60,
#             difficulty='Easy',
#             workout_type='Weights',
#             target_area='Chest',
#             equipment_access='Full Gym'
#         )
    
#     def test_get_workout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('specific-workout', args=[self.workout.pk])
#         response = self.client.get(url)
#         serialized_data = WorkoutSerializer(self.workout).data

#         # Assert workout data is returned successfully
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serialized_data)
    
#     def test_put_workout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('specific-workout', args=[self.workout.pk])
#         data = {
#             'length': 50,
#             'difficulty': 'Medium',
#             'workout_type': 'Cardio',
#             'target_area': 'Legs',
#             'equipment_access': 'No Gym'
#         }
#         response = self.client.put(url, data, format='json')

#         # Assert workout put update is successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['length'], 50)
#         self.assertEqual(response.data['difficulty'], 'Medium')
#         self.assertEqual(response.data['workout_type'], 'Cardio')
#         self.assertEqual(response.data['target_area'], 'Legs')
#         self.assertEqual(response.data['equipment_access'], 'No Gym')
    
#     def test_patch_workout_llm_call(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('specific-workout', args=[self.workout.pk])
#         data = {
#             'llm_suggested_changes': 'Add dips'
#         }
#         response = self.client.patch(url, data, format='json')

#         # Assert workout patch update is successful when a call to the llm is made
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['llm_suggested_changes'], 'Add dips')
#         self.assertEqual(len(response.data['llm_suggested_workout']), 1)

#     def test_patch_workout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('specific-workout', args=[self.workout.pk])
#         data = {
#             'workout_rating': 4
#         }
#         response = self.client.patch(url, data, format='json')

#         # Assert workout patch update is successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['workout_rating'], 4)
    
#     def test_delete_workout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         url = reverse('specific-workout', args=[self.workout.pk])
#         response = self.client.delete(url)

#         # Assert deletion is successful
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Workout.objects.filter(pk=self.workout.pk).exists())