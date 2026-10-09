"""
Admin interface configuration for the bias_analyzer application.
"""

from django.contrib import admin
from .models import JobDescriptionReview


@admin.register(JobDescriptionReview)
class JobDescriptionReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'neutrality_score',
        'bias_severity',
        'bias_direction',
        'masculine_count',
        'feminine_count',
        'total_words',
        'created_at'
    )
    list_filter = ('bias_severity', 'bias_direction', 'created_at')
    search_fields = ('title', 'original_text', 'revised_text')
    readonly_fields = (
        'total_words',
        'masculine_count',
        'feminine_count',
        'masculine_density',
        'feminine_density',
        'neutrality_score',
        'bias_severity',
        'bias_direction',
        'flagged_terms',
        'created_at'
    )
