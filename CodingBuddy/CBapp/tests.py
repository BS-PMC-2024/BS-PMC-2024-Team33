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
#from CBapp.models import CodeProblem  # Corrected import path
from django.test import TestCase, Client
from django.urls import reverse
from .models import CodeProblem
from .controller import approveCB_views
from .forms import AdminCodeProblemForm
from .models import Tutorial
from .forms import TutorialDeveloperForm

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


class AdminProblemListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('CBapp:CBstatus')
        # Create some test CodeProblem objects
        self.problem1 = CodeProblem.objects.create(
            problem="Test Problem 1",
            description="Test Description 1",
            solution="Test Solution 1",
            status="not accepted",
            language="Python"
        )
        self.problem2 = CodeProblem.objects.create(
            problem="Test Problem 2",
            description="Test Description 2",
            solution="Test Solution 2",
            status="not accepted",
            language="Java"
        )

    def test_admin_problem_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/CBstatus.html')
        self.assertIn('problems', response.context)
        self.assertEqual(len(response.context['problems']), 2)
        self.assertContains(response, self.problem1.problem)
        self.assertContains(response, self.problem2.problem)

class TutorialListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('CBapp:tutorial_list_developer')
        self.tutorial1 = Tutorial.objects.create(
            youtube_link='https://youtube.com/example1',
            medium_link='https://medium.com/example1',
            wikipedia_link='https://wikipedia.org/example1',
            language='python'
        )
        self.tutorial2 = Tutorial.objects.create(
            youtube_link='https://youtube.com/example2',
            medium_link='https://medium.com/example2',
            wikipedia_link='https://wikipedia.org/example2',
            language='java'
        )

    def test_tutorial_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/tutorial_list.html')
        self.assertIn('tutorials', response.context)
        self.assertEqual(len(response.context['tutorials']), 2)
        self.assertContains(response, self.tutorial1.youtube_link)
        self.assertContains(response, self.tutorial2.youtube_link)

    def tearDown(self):
        Tutorial.objects.all().delete()



