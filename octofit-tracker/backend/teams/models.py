from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_activities(self):
        from activities.models import Activity
        return Activity.objects.filter(user__in=self.members.all()).count()
    
    @property
    def total_calories(self):
        from activities.models import Activity
        activities = Activity.objects.filter(user__in=self.members.all())
        return sum(activity.calories_burned or 0 for activity in activities)

class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'team']
    
    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
