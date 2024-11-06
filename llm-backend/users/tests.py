from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import Mock, patch
from users.models import UserProfile



User = get_user_model()

class UserGoogleLoginTests(APITestCase):
    def setUp(self):
        # Mock the response from the Google API
        self.mock_response = {
            'email': '',
            'given_name': 'Test',
            'family_name': 'User'
        }
        self.mock_google_auth = Mock()
        self.mock_google_auth.side_effect = [self.mock_response]
        self.mock_google_auth_patcher = patch('users.views.GoogleLoginView.google_auth', self.mock_google_auth)
        self.mock_google_auth_patcher.start()
        
        # Need to create a test user and retrieve tokens, did not make it as it is too difficult to mock the google auth process

class UserProfileTests(APITestCase):
    def setUp(self):
        # Create a test user and retrieve tokens
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

    def test_get_user_profile(self):
        # Authorize with JWT token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('user_profile')
        response = self.client.get(url)

        # Assert profile data is returned successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('user_profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.put(url, data, format='json')

        # Assert profile update is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'User')

    def test_delete_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('user_profile')
        response = self.client.delete(url)

        # Assert deletion is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class UserLogoutTests(APITestCase):
    def setUp(self):
        # Create a test user and retrieve tokens
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('auth_logout')
        data = {'refresh': str(self.refresh_token)}
        response = self.client.post(url, data, format='json')

        # Assert logout is successful and token is blacklisted
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Successfully logged out', response.data['detail'])