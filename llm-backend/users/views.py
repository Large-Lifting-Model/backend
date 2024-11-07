from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.registration.views import SocialLoginView

from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from django.core.exceptions import ObjectDoesNotExist
from users.models import User, UserProfile
from users.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from backend.settings import SIMPLE_JWT



class IsAccessToken(BasePermission):
    """
    Custom permission to only allow access if the token is an access token.
    """

    def has_permission(self, request, view):
        # Extract the token from the request header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Try to decode it as an access token
                AccessToken(token)
                return True
            except TokenError:
                raise AuthenticationFailed("Only access tokens are accepted.")
        raise AuthenticationFailed("Invalid token format or missing Authorization header.")



class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        # Call the parent method to handle the token exchange with Google
        response = super().post(request, *args, **kwargs)

        # Get access token from request data
        access_token = request.data.get("access_token")
        expires_in = SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds()
        # Fetch user data from Google using the access token
        google_user_data = self.get_google_user_info(access_token)

        # Extract the email from the Google user data
        email = google_user_data.get('email')

        # Check if a user with this email already exists
        try:
            user = User.objects.get(email=email)
            print(f"User {email} found, logging in.")
            
            # Ensure the user has a profile, create one if it doesn't exist
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.is_new:
                profile.is_new = False
                profile.save()
                print(f"User {email} is a preexisting account, 'is_new' set to False.")
            else:
                print(f"User {email} is not new; 'is_new' remains False.")

        except ObjectDoesNotExist:
            # No existing user found, create a new user
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=google_user_data.get('given_name'),
                last_name=google_user_data.get('family_name'),
                password=None  # No password needed since we are using social login (Google

            )
            # Create a profile for the new user, checking if it already exists to avoid duplicate issues
            UserProfile.objects.get_or_create(user=user)
            print(f"New user {email} created and logged in.")

        # Generate JWT tokens (access and refresh) for the user
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


        return Response({"access": tokens['access'], "refresh": tokens['refresh'],"expires": expires_in}, status=status.HTTP_200_OK)

    def get_google_user_info(self, access_token):
        """
        This method fetches the user information from Google using the access token.
        """
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        return response.json()
      


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAccessToken] # Ensures only authenticated users using access token can access this API

    def get(self, request):
        # Fetch the user's profile
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        """Update the user's profile and health data."""
        try:
            profile = request.user.profile

        except ObjectDoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = request.user
            profile = user.profile  # Get the user's profile
            
            # Delete the associated profile and health data
            profile.delete()

            # Delete the user account itself
            user.delete()

            return Response({"detail": "User, profile, and health data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated, IsAccessToken] 

    def post(self, request):
        try:
            # Extract refresh token from the request
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)

            # Try to fetch the token from OutstandingToken
            try:
                outstanding_token = OutstandingToken.objects.get(token=str(token))
                # Check if the refresh token is already blacklisted
                if BlacklistedToken.objects.filter(token=outstanding_token).exists():
                    return Response({"detail": "Refresh token is already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
            except OutstandingToken.DoesNotExist:
                # If it's not in the OutstandingToken, blacklist it directly
                pass

            # Blacklist the token
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



def index(request):
    return render(request, 'users/')