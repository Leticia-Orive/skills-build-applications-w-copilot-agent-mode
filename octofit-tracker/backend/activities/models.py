from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym Workout'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    date_completed = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_completed']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.activity_type})"
