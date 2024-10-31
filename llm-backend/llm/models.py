from django.db import models

#####################
#### FOR TESTING ####
class LlmPrompt(models.Model):
    
    def idNumber():
        n = LlmPrompt.objects.count()
        if n == None:
            return 1
        else:
            return n + 1


    id = models.IntegerField(auto_created=True, primary_key= True, default = idNumber)
    prompt_text = models.TextField()
    response_text = models.TextField(default= '')




