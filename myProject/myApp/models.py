from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class Custom_User(AbstractUser):
    USER=[
        ('admin','Admin'),('student','Student')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER,max_length=120)
    otp_token = models.CharField(max_length=10, null= True, blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.display_name

class TaskCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class myTaskModel(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)

    
    def mark_as_completed(self):
        self.completed = True
        self.completed_date = timezone.now()
        self.save()
        self.title

