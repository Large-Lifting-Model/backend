from django.db import models

class LLMModel(models.Model):
    workout_text = models.TextField()

#####################
#### FOR TESTING ####
class LLMPrompt(models.Model):
    prompt_text = models.TextField()


