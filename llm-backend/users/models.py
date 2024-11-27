from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class HealthData(models.Model):
    # One-to-One relationship with the UserProfile model
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, related_name="health_data")
    # Health Information Fields
    dob = models.DateField("Date of Birth", null=True, blank=True)
    gender = models.CharField(
        "Gender",
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        null=True,
        blank=True,
    )
    height = models.FloatField("Height (in meters)", null=True, blank=True)
    weight = models.FloatField("Weight (in kilograms)", null=True, blank=True)

    # Fitness Information
    favourite_workout_type = models.CharField(
        "Favourite Workout Type",
        max_length=50,
        choices=[
            ("Resistance Training", "Resistance Training"),
            ("Cardio", "Cardio"),
            ("Circuits", "Circuits"),
            ("Crossfit", "Crossfit"),
            ("Yoga", "Yoga"),
        ],
        null=True,
        blank=True,
    )
    workout_experience = models.CharField(
        "Workout Experience",
        max_length=20,
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Expert", "Expert"),
        ],
        null=True,
        blank=True,
    )
    fitness_goal = models.CharField("Fitness Goal", max_length=255, null=True, blank=True)
    injuries = models.TextField("Injuries", null=True, blank=True)
    other_considerations = models.TextField("Other Considerations", null=True, blank=True)

    def __str__(self):
        return f"Health Data for {self.profile.user.username}"

class UserProfile(models.Model):
    # One-to-One relationship with the Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_new = models.BooleanField(default=True) # Flag to check if user has completed registration

    def __str__(self):
        return self.user.username

# Signal to create or update profile and health data automatically when a user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the user profile and health data when a new user is created
        profile = UserProfile.objects.create(user=instance)
        HealthData.objects.create(profile=profile)
    else:
        # Update profile if it exists
        if not hasattr(instance, 'profile'):
            profile = UserProfile.objects.create(user=instance)
        else:
            instance.profile.save()

        # Create health data if it doesn't exist
        if not hasattr(instance.profile, 'health_data'):
            HealthData.objects.create(profile=instance.profile)
        else:
            instance.profile.health_data.save()