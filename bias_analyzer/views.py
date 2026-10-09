"""
Views for the SDG 5 Bias-Free Job Description Reviewer.

Handles:
- Landing page with job description input form and sample presets
- Processing and executing the NLP bias analysis
- Displaying interactive results with score gauges, highlighted text, and replacements
- Review history log and UN SDG 5 educational information
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import JobDescriptionForm
from .models import JobDescriptionReview
from .utils.analyzer import JobBiasAnalyzer
from .utils.words_database import SAMPLE_JOB_DESCRIPTIONS

# Singleton analyzer instance for fast in-memory reuse
analyzer = JobBiasAnalyzer()


def index(request):
    """
    Landing Page View:
    Displays the analysis input form, SDG 5 mission overview,
    and pre-loaded sample job description selectors.
    """
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title') or "Job Description Analysis"
            original_text = form.cleaned_data.get('original_text')

            # Run rule-based NLP analyzer
            analysis_result = analyzer.analyze(original_text)

            # Persist review to database
            review = JobDescriptionReview.objects.create(
                title=title,
                original_text=original_text,
                revised_text=analysis_result['revised_text'],
                total_words=analysis_result['total_words'],
                masculine_count=analysis_result['masculine_count'],
                feminine_count=analysis_result['feminine_count'],
                masculine_density=analysis_result['masculine_density'],
                feminine_density=analysis_result['feminine_density'],
                neutrality_score=analysis_result['neutrality_score'],
                bias_severity=analysis_result['severity_level'],
                bias_direction=analysis_result['bias_direction'],
                flagged_terms=analysis_result['flagged_terms'],
            )

            messages.success(request, "Analysis completed successfully!")
            return redirect('bias_analyzer:review_detail', pk=review.pk)
        else:
            messages.error(request, "Please check the form inputs below.")
    else:
        form = JobDescriptionForm()

    context = {
        'form': form,
        'samples': SAMPLE_JOB_DESCRIPTIONS,
    }
    return render(request, 'bias_analyzer/index.html', context)


def review_detail(request, pk):
    """
    Results Dashboard View:
    Displays comprehensive analysis metrics, Gender Neutrality Index,
    inline highlighted terms with tooltip replacements, and revised copy.
    """
    review = get_object_or_404(JobDescriptionReview, pk=pk)

    # Re-run analyzer dynamically to produce the highlighted HTML view
    analysis_result = analyzer.analyze(review.original_text)

    # Prepare gauge and circle calculation for SVG progress ring
    # Circumference for r=45 is 2 * pi * 45 ≈ 282.7
    circumference = 282.7
    score = review.neutrality_score
    dash_offset = circumference - (circumference * score / 100)

    context = {
        'review': review,
        'analysis': analysis_result,
        'circumference': circumference,
        'dash_offset': dash_offset,
        'recent_reviews': JobDescriptionReview.objects.exclude(pk=review.pk)[:5],
    }
    return render(request, 'bias_analyzer/result.html', context)


def review_history(request):
    """
    History View:
    Displays previously analyzed job descriptions and their neutrality scores.
    """
    reviews = JobDescriptionReview.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'bias_analyzer/history.html', context)


@require_POST
def delete_review(request, pk):
    """Deletes a review from the database."""
    review = get_object_or_404(JobDescriptionReview, pk=pk)
    review.delete()
    messages.info(request, "Review record was removed.")
    return redirect('bias_analyzer:history')


def about_sdg5(request):
    """
    Educational View:
    Explains UN Sustainable Development Goal 5 (Gender Equality),
    the research background (Gaucher et al.), and the scoring logic.
    """
    return render(request, 'bias_analyzer/about.html')


def sample_data_api(request, sample_key):
    """
    JSON helper endpoint for frontend to inject sample texts.
    """
    sample = SAMPLE_JOB_DESCRIPTIONS.get(sample_key)
    if sample:
        return JsonResponse(sample)
    return JsonResponse({'error': 'Sample not found'}, status=404)
