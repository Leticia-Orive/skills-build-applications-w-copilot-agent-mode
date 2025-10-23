from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamListCreateView.as_view(), name='team_list_create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('<int:pk>/join/', views.JoinTeamView.as_view(), name='join_team'),
    path('<int:pk>/leave/', views.LeaveTeamView.as_view(), name='leave_team'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]