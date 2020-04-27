from django.db import models
from rest_framework import serializers
import datetime



# Create your models here.
class category(models.Model):
    cid=models.AutoField(primary_key=True)
    cname=models.CharField(max_length=100)
    #subcategory=models.CharField(max_length=100)
    def __str__(self):
        return self.cname

class product(models.Model):
    pid= models.AutoField(primary_key=True)
    logoname= models.CharField(max_length=200)
    category= models.ForeignKey(category, on_delete=models.CASCADE)
    price= models.FloatField(max_length=1000,default=0.0)
    companyname=models.CharField(max_length=200)

    def __str__(self):
        return self.companyname

class logoinfo(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,default="")
    img=models.ImageField(upload_to='upload/',default="dummy.jpg")
    category= models.ForeignKey(category, on_delete=models.CASCADE)


    def __str__(self):
        return self.title 

class client(models.Model):
    name=models.CharField(max_length=255,default="")
    email=models.CharField(max_length=255,default="")
    contact=models.IntegerField()
    message=models.TextField()
    datetime=models.DateField(default=datetime.date.today)
    mark_time=models.IntegerField(default=0) 
    logoid=models.ForeignKey(logoinfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.email

class users(models.Model):
    userid=models.AutoField(primary_key=True)
    fullname=models.CharField(max_length=255,default="")
    email=models.CharField(max_length=255,default="")
    password=models.TextField(default="0")


class SerClient(serializers.ModelSerializer):
    
    class Meta:
        model = client
        fields= '__all__'

class SerCategory(serializers.ModelSerializer):
    
    class Meta:
        model = category
        fields= '__all__'