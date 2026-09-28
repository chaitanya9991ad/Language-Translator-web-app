from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)