from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from .models import Team, TeamMembership

class TeamSerializer(ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'creator', 'members_count', 'total_activities', 'total_calories', 'created_at']
        read_only_fields = ['creator', 'created_at']
    
    def get_members_count(self, obj):
        return obj.members.count()

class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Team.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        team = serializer.save(creator=self.request.user)
        team.members.add(self.request.user)

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Team.objects.all()

class JoinTeamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        if request.user in team.members.all():
            return Response({'message': 'You are already a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        team.members.add(request.user)
        return Response({'message': 'Successfully joined the team'}, 
                       status=status.HTTP_200_OK)

class LeaveTeamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        if request.user not in team.members.all():
            return Response({'message': 'You are not a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        team.members.remove(request.user)
        return Response({'message': 'Successfully left the team'}, 
                       status=status.HTTP_200_OK)

class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from activities.models import Activity
        from django.db.models import Sum, Count
        
        # Get user stats
        users = User.objects.annotate(
            total_activities=Count('activities'),
            total_calories=Sum('activities__calories_burned')
        ).order_by('-total_calories')[:10]
        
        leaderboard_data = []
        for user in users:
            leaderboard_data.append({
                'username': user.username,
                'total_activities': user.total_activities or 0,
                'total_calories': user.total_calories or 0
            })
        
        return Response({'leaderboard': leaderboard_data})
