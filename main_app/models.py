from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=100)
    input_language = models.CharField(max_length=100)    
    textinput = models.TextField(max_length=250)
    output_language = models.CharField(max_length=100)    
    result = models.TextField(max_length=250)

    def __str__(self):
        return self.title