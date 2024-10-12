from django.db import models

DIFFICULTYS = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]

WORKOUTS = [('Weights', 'Weights'), ('Cardio', 'Cardio'), ('Circuits', 'Circuits'), 
            ('Crossfit', 'Crossfit'), ('Yoga', 'Yoga'), ('Other', 'Other') ]

TARGET_AREAS = [('Chest', 'Chest'), ('Back', 'Back'), ('Arms', 'Arms'), ('Legs', 'Legs'), ('Core', 'Core'), ('Other', 'Other')]

EQUIPMENT = [('Full Gym', 'Full Gym'), ('Limited Gym', 'Limited Gym'), ('Dumbells', 'Dumbells'), ('Nothing', 'Nothing'), ('Other', 'Other')]

class Workout(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    length = models.IntegerField()
    difficulty = models.CharField(choices=DIFFICULTYS, max_length=100)
    workout_type = models.CharField(choices=WORKOUTS, max_length=100)
    target_area = models.CharField(choices=TARGET_AREAS, max_length=100)
    included_exercises = models.TextField()
    excluded_exercises = models.TextField()
    equipment_access = models.CharField(choices=EQUIPMENT, max_length=100)
    other_considerations = models.TextField()

    # user = models.ForeignKey('users.User', on_delete=models.CASCADE) # This is a placeholder for the user model that will be created later
    

    def __str__(self):
        return self.name