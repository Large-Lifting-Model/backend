from django.contrib import admin
from .models import UserProfile, HealthData

# inline admin descriptor for HealthData to display it within UserProfile
class HealthDataInline(admin.StackedInline):
    model = HealthData
    can_delete = False
    verbose_name_plural = 'Health Data'

# Define a new UserProfile admin with the inline HealthData
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (HealthDataInline,)

# Register the UserProfile and HealthData models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HealthData)  # Register the HealthData model to the admin site