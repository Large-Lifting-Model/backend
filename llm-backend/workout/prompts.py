prompt_start = "Create a workout using the following parameters:\n"
prompt_end = """Return your response in the following json format where each workout is a seperate json object in the contents list. Each workout has a "name", the "type" of workout, and "info" about the amount of reps/sets/duration to do it in.\n
        {"content": [{
            "workout":{
                "name": "",
                "type": "",
                "info": ""
                }
            }
            ]
        }
"""
prompt_history = "For context here are the last three workouts the user has done:\n"


