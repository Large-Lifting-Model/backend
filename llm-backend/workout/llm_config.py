#Prompt formatting
prompt_start = "Create a workout using the following parameters:\n"
prompt_end = """Return your response in the following json format where each exericise is a seperate json object in the contents list. Each exercise has a "name", the "type" of workout, and "info" about the amount of reps/sets/duration to do it in.\n
Format: {"content": [{"workout":{"name": "","type": "","info": ""}}]}
"""
prompt_history = "For context here are the last three workouts the user has done:\n"

#Keys for user data
workout_keys = ["length",
                "difficulty",
                "workout_type",
                "target_area",
                "equipment_access",
                "included_exercises",
                "excluded_exercises",
                "other_workout_considerations"
                ]
health_keys = ["gender",
                "height",
                "weight",
                "favourite_workout_type",
                "workout_experience",
                "fitness_goal",
                "injuries"
                ]



