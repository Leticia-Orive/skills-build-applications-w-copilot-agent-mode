from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('', views.UserListView.as_view(), name='user_list'),
]