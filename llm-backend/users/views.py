from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from allauth.account.utils import perform_login

from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import SocialConnectView



from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from users.models import User, UserProfile
from users.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken



# @method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        # Call the parent method to handle the token exchange with Google
        response = super().post(request, *args, **kwargs)

        # Get access token from request data
        access_token = request.data.get("access_token")

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
            if created:
                print(f"Profile created for user {email}")
            else:
                print(f"Profile already exists for user {email}")

        except ObjectDoesNotExist:
            # No existing user found, create a new user
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=google_user_data.get('given_name'),
                last_name=google_user_data.get('family_name'),
                password=None  # No password needed since we are using social login
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

        return Response({"access": tokens['access'], "refresh": tokens['refresh']}, status=status.HTTP_200_OK)

    def get_google_user_info(self, access_token):
        """
        This method fetches the user information from Google using the access token.
        """
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        return response.json()
class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = settings.FACEBOOK_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"error": "Missing access token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract user info from Facebook
            user_info = self.get_facebook_user_info(access_token)
            email = user_info.get('email')
            if not email:
                return Response({"error": "Facebook account does not have an email."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a user with the same email exists
            try:
                user = User.objects.get(email=email)

                # Check if the user is already linked to Facebook
                if SocialAccount.objects.filter(user=user, provider='facebook').exists():
                    return Response({"error": "User is already registered with this email and linked to Facebook."}, status=status.HTTP_400_BAD_REQUEST)

                # If not linked, link the Facebook account to the existing user
                perform_login(request, user, email_verification='none')
                return Response({"detail": "Account linked successfully."}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                # No existing user, proceed with normal flow (create user)
                return super().post(request, *args, **kwargs)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_facebook_user_info(self, access_token):
        response = requests.get(
            f'https://graph.facebook.com/me?fields=id,email,first_name,last_name&access_token={access_token}'
        )
        return response.json()


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this API

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
    permission_classes = (IsAuthenticated,)  # Ensure only authenticated users can access this API

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

# Not needed for now since frontend is handling the callback
# @method_decorator(csrf_exempt, name='dispatch')
# class GoogleLoginCallback(APIView):
#     def get(self, request, *args, **kwargs):
#         code = request.GET.get("code")

#         if not code:
#             return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

#         # Exchange the authorization code for an access token
#         token_endpoint_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "code": code,
#             "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
#             "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
#             "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
#             "grant_type": "authorization_code",
#         }

#         response = requests.post(token_endpoint_url, data=data)

#         if response.status_code != 200:
#             return Response({"error": "Failed to exchange code for token"}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(response.json(), status=status.HTTP_200_OK)



def index(request):
    return render(request, 'users/')