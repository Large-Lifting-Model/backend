from django.urls import path, include
from .views import GoogleLoginView, UserProfileView, UserLogoutView, FacebookLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication and registration
    # path('auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),  # User registration

    # Social authentication
    path('auth/social/', include('allauth.socialaccount.urls')),  # Social login/registration
    path('auth/google/', GoogleLoginView.as_view(), name='auth_social_google'),  # Google login
    # path('auth/facebook/', FacebookLoginView.as_view(), name='facebook_login'),


    # User profile actions
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # Get, update, or delete user profile

    # Logout (JWT-specific logout endpoint)
    path('auth/logout/', UserLogoutView.as_view(), name='auth_logout'),  # Custom JWT logout

    # JWT token actions
    path('auth/token/', TokenObtainPairView.as_view(), name='auth_token_obtain'),  # Obtain JWT tokens
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),  # Refresh tokens
]