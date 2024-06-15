from django.db import models

# Create your models here.

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=250)
    tools = models.TextField()
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    project_url = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50)
    additional_details = models.TextField(blank=True)

    def __str__(self):
        return self.title
    

class Contact(models.Model):
       name = models.CharField(max_length=15)
       email = models.CharField(max_length=20)
       message = models.TextField(max_length=200)
    
       def __str__(self):
        return self.name


