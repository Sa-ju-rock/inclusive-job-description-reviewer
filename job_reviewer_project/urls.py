"""
URL Configuration for job_reviewer_project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Delegate all root and app routes to bias_analyzer
    path('', include('bias_analyzer.urls')),
]
