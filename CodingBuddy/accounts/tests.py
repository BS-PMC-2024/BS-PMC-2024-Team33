from _pytest import unittest
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse


class SignupTest(TestCase):
    def setUp(self):
        Group.objects.create(name='Student')
        Group.objects.create(name='Developer')

    def test_signup_student(self):
        response = self.client.post(reverse('signup'), {
            'username': 'teststudent',
            'email': 'teststudent@example.com',
            'password1': 'tesaosdjas231',
            'password2': 'tesaosdjas231',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='teststudent').exists())

    def test_signup_developer(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testdeveloper',
            'email': 'testdeveloper@example.com',
            'password1': 'tesaosdjas231',
            'password2': 'tesaosdsjas231',
            'role': 'developer',
            'upload_file': ''
        })
        self.assertEqual(response.status_code, 200)  # Form should be re-rendered with error
        self.assertFalse(User.objects.filter(username='testdeveloper').exists())

class LoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after successful logout

class PasswordChangeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_password_change(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'testpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful password change
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

class PasswordResetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_password_reset(self):
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful password reset request


    def setUp(self):
        self.student = User.objects.create_user(username='student', password='testpassword')
        self.developer = User.objects.create_user(username='developer', password='testpassword')
        self.admin = User.objects.create_user(username='admin', password='testpassword', is_staff=True)

        student_group = Group.objects.create(name='Student')
        developer_group = Group.objects.create(name='Developer')

        self.student.groups.add(student_group)
        self.developer.groups.add(developer_group)

    def test_student_permissions(self):
        self.client.login(username='student', password='testpassword')
        response = self.client.get(reverse('CBapp:codepage'))
        self.assertEqual(response.status_code, 200)  # Ensure student can access codepage

    def test_developer_permissions(self):
        self.client.login(username='developer', password='testpassword')
        response = self.client.get(reverse('CBapp:tutorial_list_developer'))
        self.assertEqual(response.status_code, 200)  # Ensure developer can access tutorial list

    def test_admin_permissions(self):
        self.client.login(username='admin', password='testpassword')
        response = self.client.get(reverse('CBapp:CBstatus'))
        self.assertEqual(response.status_code, 200)  # Ensure admin can access CBstatus


class UserFlowTest(TestCase):
    def setUp(self):
        # Set up the client
        self.client = Client()

        # Create groups
        self.student_group = Group.objects.create(name='Student')
        self.developer_group = Group.objects.create(name='Developer')

    def test_user_signup_login_access(self):
        # Sign up as a student
        signup_response = self.client.post(reverse('signup'), {
            'username': 'teststudent',
            'email': 'teststudent@example.com',
            'password1': 'tesaosdjas231',
            'password2': 'tesaosdjas231',
            'role': 'student'
        })
        self.assertEqual(signup_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='teststudent').exists())

        # Log in as the student
        login_response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'tesaosdjas231'
        })
        self.assertEqual(login_response.status_code, 302)

        # Access a restricted page
        restricted_page_response = self.client.get(reverse('CBapp:codepage'))
        self.assertEqual(restricted_page_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
