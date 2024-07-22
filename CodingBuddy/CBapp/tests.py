import django
import unittest
import os

# Set the DJANGO_SETTINGS_MODULE environment variable correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'CBapp.settings'

# Initialize Django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from .models import CodeProblem, Tutorial
from django.contrib.auth.models import User, Group


class ViewProblemsForStudentTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='password')
        self.student_group = Group.objects.create(name='Student')
        self.user.groups.add(self.student_group)
        self.client.login(username='student', password='password')

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
        self.url = reverse('CBapp:student_problem')

    def test_view_problems_for_student_no_filter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Problem 1')
        self.assertContains(response, 'Problem 2')
        self.assertContains(response, 'Problem 3')

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


class AdminProblemListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='password')
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='admin', password='password')

        self.url = reverse('CBapp:CBstatus')
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
        self.user = User.objects.create_user(username='developer', password='password')
        self.developer_group = Group.objects.create(name='Developer')
        self.user.groups.add(self.developer_group)
        self.client.login(username='developer', password='password')

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


class AdditionalTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.developer = User.objects.create_user(username='developer', password='password')
        self.developer_group = Group.objects.create(name='Developer')
        self.developer.groups.add(self.developer_group)
        self.client.login(username='developer', password='password')

        self.problem1 = CodeProblem.objects.create(
            problem='Problem 1',
            description='Description for Problem 1',
            solution='Solution for Problem 1',
            status='accepted',
            language='Python'
        )

    def test_add_code_problem(self):
        url = reverse('CBapp:add_code_problem')
        data = {
            'problem': 'New Problem',
            'description': 'New Description',
            'solution': 'New Solution',
            'status': 'accepted',
            'language': 'Python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CodeProblem.objects.filter(problem='New Problem').exists())

    def test_edit_code_problem(self):
        url = reverse('CBapp:edit_solution', args=[self.problem1.id])
        data = {
            'problem': 'Updated Problem',
            'description': 'Updated Description',
            'solution': 'Updated Solution',
            'status': 'accepted',
            'language': 'Python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.problem1.refresh_from_db()
        self.assertEqual(self.problem1.problem, 'Updated Problem')

    def test_delete_code_problem(self):
        url = reverse('CBapp:delete_problem', args=[self.problem1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CodeProblem.objects.filter(id=self.problem1.id).exists())

    def test_add_tutorial(self):
        url = reverse('CBapp:add_tutorial')
        data = {
            'youtube_link': 'https://youtube.com/new_tutorial',
            'medium_link': 'https://medium.com/new_tutorial',
            'wikipedia_link': 'https://wikipedia.org/new_tutorial',
            'language': 'python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tutorial.objects.filter(youtube_link='https://youtube.com/new_tutorial').exists())

    def test_edit_tutorial(self):
        tutorial = Tutorial.objects.create(
            youtube_link='https://youtube.com/tutorial',
            medium_link='https://medium.com/tutorial',
            wikipedia_link='https://wikipedia.org/tutorial',
            language='python'
        )
        url = reverse('CBapp:edit_tutorial', args=[tutorial.id])
        data = {
            'youtube_link': 'https://youtube.com/updated_tutorial',
            'medium_link': 'https://medium.com/updated_tutorial',
            'wikipedia_link': 'https://wikipedia.org/updated_tutorial',
            'language': 'python'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        tutorial.refresh_from_db()
        self.assertEqual(tutorial.youtube_link, 'https://youtube.com/updated_tutorial')





if __name__ == '__main__':
    unittest.main()
