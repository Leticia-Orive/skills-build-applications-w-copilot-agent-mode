"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Octofit Tracker API!',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'auth': '/api/auth/',
            'users': '/api/users/',
            'activities': '/api/activities/',
            'teams': '/api/teams/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/', api_root, name='api_root'),
    path('', api_root, name='root'),
]
