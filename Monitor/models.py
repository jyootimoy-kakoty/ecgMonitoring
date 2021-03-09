from django.db import models

# Create your models here.

class HospitalData(models.Model):
    hospitalID = models.TextField(max_length=15, primary_key=True)
    hospitalName = models.TextField(max_length=30)
    hospitalAddress =  models.TextField(max_length=50)

 