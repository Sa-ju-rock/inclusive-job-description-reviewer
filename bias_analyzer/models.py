"""
Database models for SDG 5 Bias-Free Job Description Reviewer.

Stores analyzed job descriptions, calculated neutrality scores,
and flagged gendered words for historical review and tracking.
"""

from django.db import models
from django.urls import reverse


class JobDescriptionReview(models.Model):
    """
    Stores an analyzed job posting along with computed metrics,
    gender neutrality score, and detected terms.
    """
    title = models.CharField(
        max_length=200,
        default="Untitled Job Description",
        help_text="Optional title or position name (e.g. 'Senior Backend Engineer')"
    )
    original_text = models.TextField(
        help_text="The raw job description text submitted for bias analysis."
    )
    revised_text = models.TextField(
        blank=True,
        help_text="Suggested inclusive version with flagged terms replaced."
    )
    
    # Quantitative Metrics
    total_words = models.PositiveIntegerField(default=0)
    masculine_count = models.PositiveIntegerField(default=0)
    feminine_count = models.PositiveIntegerField(default=0)
    masculine_density = models.FloatField(
        default=0.0,
        help_text="Percentage of total words that are masculine-coded"
    )
    feminine_density = models.FloatField(
        default=0.0,
        help_text="Percentage of total words that are feminine-coded"
    )
    
    # Neutrality & Classification
    neutrality_score = models.PositiveIntegerField(
        default=100,
        help_text="Gender Neutrality Index on a scale of 0 to 100%"
    )
    bias_severity = models.CharField(
        max_length=60,
        default="Strongly Gender-Neutral",
        help_text="Severity tier (e.g. Strongly Neutral, Mild, Moderate, High)"
    )
    bias_direction = models.CharField(
        max_length=80,
        default="Balanced",
        help_text="Directional bias (Masculine-Skewed, Feminine-Skewed, or Balanced)"
    )
    
    # Structured term breakdown stored as JSON
    flagged_terms = models.JSONField(
        default=list,
        blank=True,
        help_text="Detailed list of detected terms with counts and replacements"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Job Description Review"
        verbose_name_plural = "Job Description Reviews"

    def __str__(self):
        return f"{self.title} (Score: {self.neutrality_score}%) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def get_absolute_url(self):
        return reverse('bias_analyzer:review_detail', kwargs={'pk': self.pk})

    @property
    def score_color(self):
        """Returns color theme based on score for templates."""
        if self.neutrality_score >= 90:
            return 'emerald'
        elif self.neutrality_score >= 70:
            return 'blue'
        elif self.neutrality_score >= 50:
            return 'amber'
        return 'rose'
