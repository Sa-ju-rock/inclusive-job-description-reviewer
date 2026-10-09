"""
Automated unit tests for the bias_analyzer application.
Tests analyzer logic, form validation, and views.
"""

from django.test import TestCase, Client
from django.urls import reverse
from bias_analyzer.models import JobDescriptionReview
from bias_analyzer.utils.analyzer import JobBiasAnalyzer


class AnalyzerLogicTests(TestCase):
    def setUp(self):
        self.analyzer = JobBiasAnalyzer()

    def test_masculine_detection(self):
        text = "We want a rockstar ninja developer who can dominate the market and crush bugs."
        result = self.analyzer.analyze(text)
        self.assertGreater(result['masculine_count'], 0)
        self.assertEqual(result['feminine_count'], 0)
        self.assertIn('rockstar', [t['base_word'] for t in result['flagged_terms']])
        self.assertIn('ninja', [t['base_word'] for t in result['flagged_terms']])
        self.assertLess(result['neutrality_score'], 50)

    def test_feminine_detection(self):
        text = "We need a warm, gentle, and caring teammate to nurture our users with supportive care."
        result = self.analyzer.analyze(text)
        self.assertGreater(result['feminine_count'], 0)
        self.assertEqual(result['masculine_count'], 0)
        self.assertIn('nurture', [t['base_word'] for t in result['flagged_terms']])
        self.assertIn('supportive', [t['base_word'] for t in result['flagged_terms']])
        self.assertLess(result['neutrality_score'], 50)

    def test_neutral_text(self):
        text = (
            "We are seeking a Software Engineer to design, build, and deploy RESTful APIs. "
            "You will partner with product managers and maintain high code quality."
        )
        result = self.analyzer.analyze(text)
        self.assertEqual(result['masculine_count'], 0)
        self.assertEqual(result['feminine_count'], 0)
        self.assertEqual(result['neutrality_score'], 100)
        self.assertEqual(result['severity_level'], "Strongly Gender-Neutral")

    def test_replacement_generation(self):
        text = "We need a rockstar engineer."
        result = self.analyzer.analyze(text)
        # Top replacement for rockstar is 'skilled professional'
        self.assertIn("skilled professional", result['revised_text'].lower())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_get(self):
        response = self.client.get(reverse('bias_analyzer:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SDG 5")
        self.assertContains(response, "Eliminate Gender Bias")

    def test_index_post_valid(self):
        data = {
            'title': 'Test Tech Lead',
            'original_text': 'We need a rockstar developer to lead our engineering division and build reliable microservices with Python and Django.'
        }
        response = self.client.post(reverse('bias_analyzer:index'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Should have created a JobDescriptionReview object
        review = JobDescriptionReview.objects.first()
        self.assertIsNotNone(review)
        self.assertEqual(review.title, 'Test Tech Lead')
        self.assertContains(response, "Audit Report #")
        self.assertContains(response, "Neutrality Index")

    def test_index_post_invalid_short_text(self):
        data = {
            'title': 'Too Short',
            'original_text': 'hi'
        }
        response = self.client.post(reverse('bias_analyzer:index'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a job description with at least 20 characters")

    def test_history_view(self):
        JobDescriptionReview.objects.create(
            title="DevOps Role",
            original_text="We need a competent devops engineer with kubernetes experience.",
            neutrality_score=95,
            bias_severity="Strongly Gender-Neutral",
            total_words=10,
        )
        response = self.client.get(reverse('bias_analyzer:history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DevOps Role")
        self.assertContains(response, "95%")

    def test_about_view(self):
        response = self.client.get(reverse('bias_analyzer:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gaucher et al.")
        self.assertContains(response, "Gender Neutrality Index")
