"""
URL patterns for the bias_analyzer application.
"""

from django.urls import path
from . import views

app_name = 'bias_analyzer'

urlpatterns = [
    # Landing page & Submission form
    path('', views.index, name='index'),

    # Analysis results dashboard
    path('review/<int:pk>/', views.review_detail, name='review_detail'),

    # History & Management
    path('history/', views.review_history, name='history'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),

    # UN SDG 5 Education & Research Page
    path('about/', views.about_sdg5, name='about'),

    # Helper API for quick sample loading
    path('api/sample/<str:sample_key>/', views.sample_data_api, name='sample_data'),
]
