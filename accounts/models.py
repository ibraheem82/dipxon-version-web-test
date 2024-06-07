from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

 # ===> Creating a model for super admin
#  ===>  Creating a custom user model
class User(AbstractUser):
    email = models.EmailField(unique = True)
    username = models.CharField(max_length = 100)
    bio = models.CharField(max_length = 100)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email