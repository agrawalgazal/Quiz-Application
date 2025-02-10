from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

import datetime


class Topic(models.Model):
    levels=[
        ('E','Easy'),
        ('M','Medium'),
        ('H','Hard'),
        ('X','Expert')
        ]
    quiz_id=models.BigAutoField(primary_key=True)
    topic_name=models.CharField(max_length=70)
    rating=models.DecimalField(max_digits=2,decimal_places=1,validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
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
       quiz_id=models.ForeignKey(Topic,on_delete=models.CASCADE)
       question=models.CharField(max_length=400)
       optionA=models.CharField(max_length=200)
       optionB=models.CharField(max_length=200)
       optionC=models.CharField(max_length=200)
       optionD=models.CharField(max_length=200)
       correct_ans=models.CharField(max_length=200)
       

       def __str__(self):
             return self.question
       
class UserResponse(models.Model):
      user_response_id = models.AutoField(primary_key=True)
      user_ans=models.CharField(max_length=200)
      question_response_time=models.IntegerField()
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      quiz_id=models.ForeignKey(Quiz,on_delete=models.CASCADE)
      question_id=models.ForeignKey(Question,on_delete=models.CASCADE)
      attempt_number=models.IntegerField()
      class Meta:
            unique_together=("user","quiz_id","question_id","attempt_number")

      def __str__(self):
           return f"{self.question_id.question}  response is {self.user_ans}"


             

class Point(models.Model):
      user_id=models.ForeignKey(User,on_delete=models.CASCADE)
      quiz_id=models.ForeignKey(Quiz,on_delete=models.CASCADE)
      attempt_number=models.IntegerField()
      quiz_points=models.DecimalField(max_digits=10,decimal_places=3)
      quiz_time=models.IntegerField()

      class Meta:
            unique_together=("user_id","quiz_id","attempt_number")

      def __str__(self):
             return self.user_id.username


class Attempt(models.Model):
      user_id=models.ForeignKey(User,on_delete=models.CASCADE)
      quiz_id=models.ForeignKey(Quiz,on_delete=models.CASCADE)
      number_of_attempt=models.IntegerField()
      best_point=models.DecimalField(max_digits=10,decimal_places=3)
      class Meta:
            unique_together=("user_id","quiz_id")

      def __str__(self):
            return self.user_id.username


class Global_Points(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    total_points=models.DecimalField(max_digits=10,decimal_places=3)




