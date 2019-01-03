from django.db import models
from django import forms
from django.contrib.auth.models import User
from users.choices import *
from multiselectfield import MultiSelectField

#the class 'profile' contains all of the fields in the table that is used to generate the 'Profile' page for the user.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    hobbies = MultiSelectField(choices=HOBBY_CHOICES)

    def __str__(self): #displays the name of the user
        return f'{self.user.username} Profile'
