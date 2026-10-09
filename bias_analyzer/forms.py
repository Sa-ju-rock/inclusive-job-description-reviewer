"""
Forms for the bias_analyzer application.

Includes validation, custom widgets styled with Tailwind CSS,
and helper presets for sample text evaluation.
"""

from django import forms
from .models import JobDescriptionReview


class JobDescriptionForm(forms.ModelForm):
    """
    Form for submitting job descriptions to be analyzed for gender bias.
    """
    title = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': (
                    'w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-700 '
                    'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
                    'focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none '
                    'transition-all duration-200 shadow-sm text-sm'
                ),
                'placeholder': 'e.g., Senior Full-Stack Engineer, Lead Product Manager',
            }
        ),
        label="Job Title (Optional)",
        help_text="Give this posting a title to identify it in your review history."
    )

    original_text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': (
                    'w-full px-4 py-4 rounded-xl border border-gray-300 dark:border-gray-700 '
                    'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
                    'focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none '
                    'transition-all duration-200 shadow-sm font-sans text-sm leading-relaxed'
                ),
                'rows': 12,
                'placeholder': (
                    'Paste your job description here...\n\n'
                    'Include role responsibilities, required qualifications, and company culture '
                    'sections to test for subtle gendered wording.'
                ),
                'id': 'job-description-textarea'
            }
        ),
        label="Job Description Text",
    )

    class Meta:
        model = JobDescriptionReview
        fields = ['title', 'original_text']

    def clean_original_text(self):
        text = self.cleaned_data.get('original_text', '').strip()
        if len(text) < 20:
            raise forms.ValidationError(
                "Please enter a job description with at least 20 characters for meaningful analysis."
            )
        word_count = len(text.split())
        if word_count < 5:
            raise forms.ValidationError(
                "Please provide at least 5 words so our NLP analyzer can evaluate linguistic patterns."
            )
        return text
