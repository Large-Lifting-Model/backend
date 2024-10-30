from django.db import models

# Workout model parameter choices

DIFFICULTYS = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]

WORKOUTS = [('Weights', 'Weights'), ('Cardio', 'Cardio'), ('Circuits', 'Circuits'), 
            ('Crossfit', 'Crossfit'), ('Yoga', 'Yoga'), ('Other', 'Other') ]

TARGET_AREAS = [('Chest', 'Chest'), ('Back', 'Back'), ('Arms', 'Arms'), ('Legs', 'Legs'), 
                ('Core', 'Core'), ('Other', 'Other')]

EQUIPMENT = [('Full Gym', 'Full Gym'), ('Limited Gym', 'Limited Gym'), ('Dumbells', 'Dumbells'), 
             ('Nothing', 'Nothing'), ('Other', 'Other')]

class Workout(models.Model):
    # user as foreign key

    # Required fields
    created = models.DateTimeField('Date Created', auto_now_add=True, blank=False, null=False)
    length = models.IntegerField('Length of Workout', blank=False, null=False)
    difficulty = models.CharField('Difficulty', choices=DIFFICULTYS, max_length=100, blank=False, null=False)
    workout_type = models.CharField('Workout Type', choices=WORKOUTS, max_length=100, blank=False, null=False)
    target_area = models.CharField('Target Area', choices=TARGET_AREAS, max_length=100, blank=False, null=False)
    equipment_access = models.CharField('Equipment Access', choices=EQUIPMENT, max_length=100, blank=False, null=False)
    # llm text field
    # Optional fields
    included_exercises = models.TextField('Included Exercises', blank=True, null=True)
    excluded_exercises = models.TextField('Excluded Exercises', blank=True, null=True)
    other_considerations = models.TextField('Other Considerations', blank=True, null=True)
    # llm feedback
    # extra columns for others options?    

    def __str__(self):
        return self.name