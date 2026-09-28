from django.db import models
from django.shortcuts import render

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)

def index(request):
    return render(request, 'index.html')