from django.urls import path
from . import views

urlpatterns = [
    path('', views.ActivityListCreateView.as_view(), name='activity_list_create'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('my-activities/', views.MyActivitiesView.as_view(), name='my_activities'),
]