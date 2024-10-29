from django.db import models

# Create workout models here.

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    duration = models.IntegerField()
    calories = models.IntegerField()
    time = models.TimeField()

    # user = models.ForeignKey('users.User', on_delete=models.CASCADE) # This is a placeholder for the user model that will be created later
    

    def __str__(self):
        return self.name