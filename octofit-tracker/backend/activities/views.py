from django.shortcuts import render
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from .models import Activity

class ActivitySerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.all().order_by('-date_completed')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

class MyActivitiesView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
