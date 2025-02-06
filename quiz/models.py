from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

import datetime


# Create your models here.
class Topic(models.Model):
    quiz_id=models.BigAutoField(primary_key=True)
    topic_name=models.CharField(max_length=70)
    rating=models.DecimalField(max_digits=2,decimal_places=1,validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    levels=[
        ('E','Easy'),
        ('M','Medium'),
        ('H','Hard'),
        ('X','Expert')
        ]
    difficulty_level=models.CharField(max_length=1, choices=levels, default='E')

    def __str__(self):
        return self.topic_name
    
class Quiz(models.Model):
        quiz_id=models.ForeignKey(Topic,on_delete=models.CASCADE,primary_key=True)
        quiz_accuracy=models.DecimalField(max_digits=4,decimal_places=2,validators=[MinValueValidator(0.00),MaxValueValidator(99.99)])

        def __str__(self):
             return self.quiz_id.topic_name
        
    
class Question(models.Model):
       question_id=models.BigAutoField(primary_key=True)
       topic_id=models.ForeignKey(Topic,on_delete=models.CASCADE)
       question=models.CharField(max_length=200)
       optionA=models.CharField(max_length=200)
       optionB=models.CharField(max_length=200)
       optionC=models.CharField(max_length=200)
       optionD=models.CharField(max_length=200)
       correct_ans=models.CharField(max_length=200)

       def __str__(self):
             return self.question
       
class UserResponse(models.Model):
      user_response_id=models.BigAutoField(primary_key=True)
      user_ans=models.CharField(max_length=200)
      question_response_time=models.IntegerField()
      user_id=models.ForeignKey(User,on_delete=models.CASCADE)
      quiz_id=models.ForeignKey(Quiz,on_delete=models.CASCADE)
      question_id=models.ForeignKey(Question,on_delete=models.CASCADE)
    #   attempt_number
             


