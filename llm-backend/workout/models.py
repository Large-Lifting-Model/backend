from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

'''Workout model parameter choices'''
DIFFICULTIES = [('Easy', 'Easy'), 
               ('Medium', 'Medium'), 
               ('Hard', 'Hard')]

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField('Date Created', auto_now_add=True, blank=False, null=False)


    '''Fields to be sent to the LLM'''
    # Required fields
    difficulty = models.CharField('Difficulty', choices=DIFFICULTIES, max_length=100, blank=False, null=False)
    workout_type = models.CharField('Workout Type', max_length=100, blank=False, null=False)
    equipment_access = models.CharField('Equipment Access', max_length=100, blank=False, null=False)

    # Optional fields
    target_area = models.CharField('Target Area', max_length=100, blank=True, null=True)
    length = models.IntegerField('Length of Workout (minutes)', blank=True, null=True)
    included_exercises = models.TextField('Included Exercises', blank=True, null=True)
    excluded_exercises = models.TextField('Excluded Exercises', blank=True, null=True)
    other_workout_considerations = models.TextField('Other Workout Considerations', blank=True, null=True)
    
    '''LLM generated fields'''
    # Feedback sent to llm for workout revisions, not sent in first interaction with llm
    llm_suggested_changes = ArrayField(models.TextField(), default=list, blank=True, null=True)
    # LLM generated workouts that have not been accepted by the user
    llm_suggested_workout = ArrayField(models.TextField(), default=list, blank=True, null=True)
    
    '''Feedback fields'''
    workout_rating = models.IntegerField('Workout Rating', choices=[(i, str(i)) for i in range(6)], blank=True, null=True)
    workout_comments = models.TextField('Workout Feedback', blank=True, null=True)
    actual_length = models.IntegerField('Final Length of Workout (minutes)', blank=True, null=True)
    

    def __str__(self):
        return f"Workout {self.id} by {self.user.username} on {self.created.strftime('%Y-%m-%d %H:%M')}"
    
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField('Date Created', auto_now_add=True, blank=False, null=False)
    recommendation = models.TextField('Daily Recommendation', blank = True, null = False)

    

