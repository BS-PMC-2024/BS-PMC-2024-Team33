# CBapp/tests.py

import django
import unittest
import os

# Set the DJANGO_SETTINGS_MODULE environment variable correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'CBapp.settings'

# Initialize Django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from CBapp.models import CodeProblem  # Corrected import path

class ViewProblemsForStudentTest(TestCase):

    def setUp(self):
        # Set up the client
        self.client = Client()

        # Create sample problems
        self.problem1 = CodeProblem.objects.create(
            problem='Problem 1',
            description='Description for Problem 1',
            solution='Solution for Problem 1',
            status='accepted',
            language='Python'
        )
        self.problem2 = CodeProblem.objects.create(
            problem='Problem 2',
            description='Description for Problem 2',
            solution='Solution for Problem 2',
            status='accepted',
            language='Java'
        )
        self.problem3 = CodeProblem.objects.create(
            problem='Problem 3',
            description='Description for Problem 3',
            solution='Solution for Problem 3',
            status='not accepted',
            language='Python'
        )

        # URL for the view
        self.url = reverse('CBapp:student_problem')  # Correct URL name

    def test_view_problems_for_student_no_filter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Problem 1')
        self.assertContains(response, 'Problem 2')
        self.assertNotContains(response, 'Problem 3')

    def test_view_problems_for_student_filter_python(self):
        response = self.client.get(self.url, {'language': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Problem 1')
        self.assertNotContains(response, 'Problem 2')
        self.assertNotContains(response, 'Problem 3')

    def test_view_problems_for_student_filter_java(self):
        response = self.client.get(self.url, {'language': 'Java'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Problem 2')
        self.assertNotContains(response, 'Problem 1')
        self.assertNotContains(response, 'Problem 3')

if __name__ == '__main__':
    unittest.main()
