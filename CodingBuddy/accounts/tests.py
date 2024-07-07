from django.test import TestCase
from django.contrib.auth.models import User, Group

class SignupTest(TestCase):
    def setUp(self):
        Group.objects.create(name='Student')
        Group.objects.create(name='Developer')

    def test_signup_student(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'teststudent',
            'email': 'teststudent@example.com',
            'password1': 'tesaosdjas231',
            'password2': 'tesaosdjas231',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='teststudent').exists())

    def test_signup_developer(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'testdeveloper',
            'email': 'testdeveloper@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'role': 'developer',
            'upload_file': ''
        })
        self.assertEqual(response.status_code, 200)  # Form should be re-rendered with error
        self.assertFalse(User.objects.filter(username='testdeveloper').exists())
