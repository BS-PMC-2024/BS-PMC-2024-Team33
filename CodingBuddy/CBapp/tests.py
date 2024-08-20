import datetime
import unittest

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from .models import CodeProblem, Tutorial, Comment, Message
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Tutorial
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CodeProblem, Comment
from .forms import CommentForm
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.html import escape
from unittest.mock import patch, MagicMock
from CBapp.models import CodeProblem, Comment
from CBapp.forms import ProblemFilterForm, CommentForm
import markdown
from django.utils.safestring import mark_safe
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import CodeProblem, Comment
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from CBapp.models import CodeProblem
from CBapp.forms import CodeProblemForm
from django.test import TestCase, Client
from django.urls import reverse
from CBapp.models import Tutorial
from .controller.tutorials_views import tutorial_list_student
from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import ValidationError
from unittest.mock import patch
from CBapp.models import CodeProblem
from CBapp.forms import CodeProblemForm


from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from CBapp.models import CodeProblem
from CBapp.forms import CodeProblemForm
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from CBapp.forms import MessageForm
from CBapp.models import Message


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from CBapp.models import CodeProblem, Solution
from CBapp.forms import SolutionForm
from unittest.mock import patch





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
        self.url = reverse('CBapp:codepage')

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
        self.assertNotContains(response, 'Problem 1')
        self.assertContains(response, 'Problem 2')
        self.assertNotContains(response, 'Problem 3')


class AdminProblemListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='password')
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='admin', password='password')

        self.url = reverse('CBapp:codepage')
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
        self.assertIn('code_problems', response.context)
        self.assertEqual(len(response.context['code_problems']), 2)
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
        self.assertIn('tutorials', response.context)
        self.assertEqual(len(response.context['tutorials']), 2)
        self.assertContains(response, self.tutorial1.youtube_link)
        self.assertContains(response, self.tutorial2.youtube_link)

    def tearDown(self):
        Tutorial.objects.all().delete()


class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_homepage_view(self):
        response = self.client.get(reverse('CBapp:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/homepage.html')

    def test_codepage_view(self):
        response = self.client.get(reverse('CBapp:codepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/codepage.html')

    def test_addcodepage_view(self):
        response = self.client.get(reverse('CBapp:addcodepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/addcodepage.html')

    def test_tutorial_list_developer_view(self):
        response = self.client.get(reverse('CBapp:tutorial_list_developer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/tutorial_list.html')

    def test_add_tutorial_view(self):
        response = self.client.get(reverse('CBapp:add_tutorial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/add_tutorial.html')

    def test_edit_tutorial_view(self):
        tutorial = Tutorial.objects.create(title='Sample Tutorial', content='Tutorial Content')
        response = self.client.get(reverse('CBapp:edit_tutorial', args=[tutorial.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/edit_tutorial.html')

    def test_chat_page_view(self):
        response = self.client.get(reverse('CBapp:chat_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_page.html')


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_update_password(self):
        response = self.client.post(reverse('profile'), {
            'username': self.user.username,
            'email': self.user.email,
            'old_password': 'password',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirects after successful update
        self.assertTrue(self.user.check_password('newpassword'))


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_add_comment(self):
        problem = CodeProblem.objects.create(problem='Sample Problem', description='Sample Description')
        response = self.client.post(reverse('CBapp:add_comment', args=[problem.id]), {
            'content': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful comment addition

    def test_delete_comment(self):
        problem = CodeProblem.objects.create(problem='Sample Problem', description='Sample Description')
        comment = Comment.objects.create(user=self.user, problem=problem, content='Comment to delete')
        response = self.client.post(reverse('CBapp:delete_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 204)  # Successful deletion

    def test_edit_comment(self):
        problem = CodeProblem.objects.create(problem='Sample Problem', description='Sample Description')
        comment = Comment.objects.create(user=self.user, problem=problem, content='Original comment')
        response = self.client.post(reverse('CBapp:edit_comment', args=[comment.id]), {
            'content': 'Updated comment'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful update
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')


class MessageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_send_message(self):
        user2 = User.objects.create_user(username='user2', password='password')
        response = self.client.post(reverse('CBapp:send_message'), {
            'receiver': user2.id,
            'content': 'Hello, user2!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful message send

    def test_receive_message(self):
        user2 = User.objects.create_user(username='user2', password='password')
        message = Message.objects.create(sender=self.user, receiver=user2, content='Hello, user2!',
                                         timestamp=datetime.datetime.now())
        self.assertEqual(message.content, 'Hello, user2!')
        self.assertEqual(message.sender.username, 'testuser')
        self.assertEqual(message.receiver.username, 'user2')


class CodeProblemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_add_code_problem(self):
        response = self.client.post(reverse('CBapp:add_code_problem'), {
            'problem': 'New Problem',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful addition
        problem = CodeProblem.objects.get(problem='New Problem')
        self.assertEqual(problem.description, 'New Description')

    def test_delete_code_problem(self):
        problem = CodeProblem.objects.create(problem='Sample Problem', description='Sample Description')
        response = self.client.post(reverse('CBapp:delete_problem', args=[problem.id]), {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 204)  # Successful deletion
        self.assertFalse(CodeProblem.objects.filter(problem='Sample Problem').exists())


class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        Group.objects.create(name='Developer')

    def test_homepage_view(self):
        response = self.client.get(reverse('CBapp:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/homepage.html')

    def test_codepage_view(self):
        response = self.client.get(reverse('CBapp:codepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/codepage.html')

    def test_addcodepage_view(self):
        response = self.client.get(reverse('CBapp:add_code_problem'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/addcodepage.html')

    def test_tutorial_list_developer_view(self):
        response = self.client.get(reverse('CBapp:tutorial_list_developer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/tutorial_list.html')

    def test_add_tutorial_view(self):
        response = self.client.get(reverse('CBapp:add_tutorial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/add_tutorial.html')

    def test_edit_tutorial_view(self):
        tutorial = Tutorial.objects.create(youtube_link='Sample Tutorial', medium_link='Tutorial Content',
                                           wikipedia_link='las;kd', language='Python')
        response = self.client.get(reverse('CBapp:edit_tutorial', args=[tutorial.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/edit_tutorial.html')

    def test_chat_page_view(self):
        response = self.client.get(reverse('CBapp:chat_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_page.html')


class IntegrationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')

    def test_profile_comment_message_integration(self):
        # Update profile
        self.client.post(reverse('profile'), {
            'username': 'user1_new',
            'email': self.user1.email,
            'old_password': '',
            'new_password1': '',
            'new_password2': ''
        })
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'user1_new')

        # Add comment
        problem = CodeProblem.objects.create(problem='Sample Problem', description='Sample Description')
        response = self.client.post(reverse('CBapp:add_comment', args=[problem.id]), {
            'content': 'Integration test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful comment addition

        # Send message
        user2 = User.objects.create_user(username='user2', password='password')
        response = self.client.post(reverse('CBapp:send_message'), {
            'receiver': user2.id,
            'content': 'Hello, user2!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful message send
        message = Message.objects.get(receiver=user2, content='Hello, user2!')
        self.assertEqual(message.sender.username, 'user1_new')

    def test_view_code_problems(self):
        # Test that code problems are displayed correctly
        CodeProblem.objects.create(problem='Problem 1', description='Description 1')
        CodeProblem.objects.create(problem='Problem 2', description='Description 2')
        response = self.client.get(reverse('CBapp:codepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Problem 1')
        self.assertContains(response, 'Problem 2')


class TutorialListDeveloperViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a developer user and add them to the 'Developer' group
        self.developer_user = User.objects.create_user(username='devuser', password='password')
        developer_group = Group.objects.create(name='Developer')
        self.developer_user.groups.add(developer_group)

        # Create some tutorials with different languages and content
        self.tutorial_python = Tutorial.objects.create(language='python', youtube_link='https://www.youtube.com/python',
                                                       medium_link='', wikipedia_link='')
        self.tutorial_java = Tutorial.objects.create(language='java', youtube_link='https://www.youtube.com/java',
                                                     medium_link='', wikipedia_link='')
        self.tutorial_c = Tutorial.objects.create(language='c', youtube_link='https://www.youtube.com/c',
                                                  medium_link='', wikipedia_link='')

    def test_tutorial_list_with_filter_python(self):
        # Login as the developer user
        self.client.login(username='devuser', password='password')

        # Make a GET request with a language filter for Python
        response = self.client.get(reverse('CBapp:tutorial_list_developer'), {'language': 'python'})

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response contains the Python tutorial
        self.assertContains(response, 'https://www.youtube.com/python')

        # Assert the response does not contain the Java or C tutorial
        self.assertNotContains(response, 'https://www.youtube.com/java')
        self.assertNotContains(response, 'https://www.youtube.com/c')

    def test_tutorial_list_with_filter_java(self):
        # Login as the developer user
        self.client.login(username='devuser', password='password')

        # Make a GET request with a language filter for Java
        response = self.client.get(reverse('CBapp:tutorial_list_developer'), {'language': 'java'})

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response contains the Java tutorial
        self.assertContains(response, 'https://www.youtube.com/java')

        # Assert the response does not contain the Python or C tutorial
        self.assertNotContains(response, 'https://www.youtube.com/python')
        self.assertNotContains(response, 'https://www.youtube.com/c')



class EditTutorialViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a developer user and a tutorial to edit
        self.developer_user = User.objects.create_user(username='devuser', password='password')

        # Add the user to the 'Developer' group
        developer_group = Group.objects.create(name='Developer')
        self.developer_user.groups.add(developer_group)

        # Create a tutorial
        self.tutorial = Tutorial.objects.create(language='python', youtube_link='https://www.youtube.com/python')

        # Login the user
        self.client.login(username='devuser', password='password')

    def test_edit_tutorial_get(self):
        # Simulate a GET request to retrieve the edit form
        response = self.client.get(reverse('CBapp:edit_tutorial', args=[self.tutorial.id]))

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the correct template is used
        self.assertTemplateUsed(response, 'developer/edit_tutorial.html')

        # Assert the form is pre-filled with the correct data
        form = response.context['form']
        self.assertEqual(form.instance, self.tutorial)

    def test_edit_tutorial_post_valid_data(self):
        # Simulate a POST request to edit the tutorial with valid data
        response = self.client.post(reverse('CBapp:edit_tutorial', args=[self.tutorial.id]), {
            'language': 'java',
            'youtube_link': 'https://www.youtube.com/java',
        })

        # Assert the tutorial was successfully edited and redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('CBapp:tutorial_list_developer'))

        # Assert the tutorial was updated in the database
        self.tutorial.refresh_from_db()
        self.assertEqual(self.tutorial.language, 'java')
        self.assertEqual(self.tutorial.youtube_link, 'https://www.youtube.com/java')

    def test_edit_tutorial_post_invalid_data(self):
        # Simulate a POST request with invalid data (e.g., missing required fields)
        response = self.client.post(reverse('CBapp:edit_tutorial', args=[self.tutorial.id]), {
            'language': '',  # Invalid because it's required
            'youtube_link': 'https://www.youtube.com',
        })

        # Assert the response status code is 200 (form is re-rendered with errors)
        self.assertEqual(response.status_code, 200)

        # Assert the form contains errors
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('language', form.errors)
        self.assertIn('This field is required.', form.errors['language'])

        # Assert the tutorial has not been updated in the database
        self.tutorial.refresh_from_db()
        self.assertEqual(self.tutorial.language, 'python')  # No change



class AddTutorialViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a developer user
        self.developer_user = User.objects.create_user(username='devuser', password='password')

    def test_add_tutorial_post(self):
        # Login as the developer user
        self.client.login(username='devuser', password='password')

        # Simulate a POST request to add a new tutorial
        response = self.client.post(reverse('CBapp:add_tutorial'), {
            'language': 'python',
            'youtube_link': 'https://www.youtube.com',
        })

        # Assert the tutorial was successfully added and redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('CBapp:tutorial_list_developer'))

        # Assert that the tutorial exists in the database
        self.assertEqual(Tutorial.objects.count(), 1)
        self.assertEqual(Tutorial.objects.first().language, 'python')




class TutorialListStudentViewTest(TestCase):

    def setUp(self):
        # Create a client instance
        self.client = Client()

        # Create some tutorials with different languages
        Tutorial.objects.create(language='python', youtube_link='https://www.youtube.com/python')
        Tutorial.objects.create(language='java', youtube_link='https://www.youtube.com/java')
        Tutorial.objects.create(language='c', youtube_link='https://www.youtube.com/c')

    def test_tutorial_list_without_filter(self):
        # Simulate a GET request without any language filter
        response = self.client.get(reverse('CBapp:tutorial_list_student'))

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert that all tutorials are listed in the context
        self.assertEqual(len(response.context['tutorials']), 3)
        # Assert the template used
        self.assertTemplateUsed(response, 'student/tutorial_list.html')

    def test_tutorial_list_with_filter_python(self):
        # Simulate a GET request with a language filter for Python
        response = self.client.get(reverse('CBapp:tutorial_list_student'), {'language': 'python'})

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert only the Python tutorial is listed in the context
        self.assertEqual(len(response.context['tutorials']), 1)
        self.assertEqual(response.context['tutorials'][0].language, 'python')
        # Assert the selected language is set correctly in the context
        self.assertEqual(response.context['selected_language'], 'python')

    def test_tutorial_list_with_filter_java(self):
        # Simulate a GET request with a language filter for Java
        response = self.client.get(reverse('CBapp:tutorial_list_student'), {'language': 'java'})

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert only the Java tutorial is listed in the context
        self.assertEqual(len(response.context['tutorials']), 1)
        self.assertEqual(response.context['tutorials'][0].language, 'java')
        # Assert the selected language is set correctly in the context
        self.assertEqual(response.context['selected_language'], 'java')


class DeleteProblemTest(TestCase):
    def setUp(self):
        # Create a staff user (authorized user)
        self.staff_user = User.objects.create_user(
            username='staff_user', password='password123', is_staff=True
        )

        # Create a non-staff user (unauthorized user)
        self.regular_user = User.objects.create_user(
            username='regular_user', password='password123', is_staff=False
        )

        # Create a sample CodeProblem instance
        self.problem = CodeProblem.objects.create(
            problem='Sample Problem',
            description='Sample Description',
            solution='Sample Solution',
            status='Open',
            language='Python'
        )

        # URL for deleting the problem
        self.url = reverse('CBapp:delete_problem', kwargs={'problem_id': self.problem.id})

    def test_delete_problem_as_staff(self):
        # Log in as staff user
        self.client.login(username='staff_user', password='password123')

        # Send a POST request to delete the problem
        response = self.client.post(self.url)

        # Check that the problem is deleted
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CodeProblem.objects.filter(id=self.problem.id).count(), 0)

    def test_delete_problem_as_non_staff(self):
        # Log in as a non-staff user
        self.client.login(username='regular_user', password='password123')

        # Send a POST request to delete the problem
        response = self.client.post(self.url)

        # Check that the response is 403 Forbidden
        self.assertEqual(response.status_code, 403)

        # Ensure that the problem still exists
        self.assertEqual(CodeProblem.objects.filter(id=self.problem.id).count(), 1)

    def test_delete_problem_as_unauthenticated_user(self):
        # Send a POST request to delete the problem without logging in
        response = self.client.post(self.url)

        # Check that the response is 403 Forbidden
        self.assertEqual(response.status_code, 403)

        # Ensure that the problem still exists
        self.assertEqual(CodeProblem.objects.filter(id=self.problem.id).count(), 1)



class AddCodeProblemTest(TestCase):
    def setUp(self):
        # Create a staff user (authorized user)
        self.staff_user = User.objects.create_user(
            username='staff_user', password='password123', is_staff=True
        )

        # Create a non-staff user (unauthorized user)
        self.regular_user = User.objects.create_user(
            username='regular_user', password='password123', is_staff=False
        )

        # URL for adding a code problem
        self.url = reverse('CBapp:add_code_problem')

    def test_add_code_problem_as_staff_user_valid_form(self):
        # Log in as staff user
        self.client.login(username='staff_user', password='password123')

        # Data for the valid form
        form_data = {
            'problem': 'Sample Problem',
            'description': 'Sample Description',
            'solution': 'Sample Solution',
            'status': 'Open',
            'language': 'Python'
        }

        # Send a POST request with valid form data
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to the code page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertRedirects(response, reverse('CBapp:codepage'))

        # Check that the problem was saved in the database
        self.assertTrue(CodeProblem.objects.filter(problem='Sample Problem').exists())

    def test_add_code_problem_as_staff_user_invalid_form(self):
        # Log in as staff user
        self.client.login(username='staff_user', password='password123')

        # Data for the invalid form (missing required fields)
        form_data = {
            'problem': '',  # Invalid: empty problem field
            'description': 'Sample Description',
            'solution': 'Sample Solution',
            'status': 'Open',
            'language': 'Python'
        }

        # Send a POST request with invalid form data
        response = self.client.post(self.url, form_data)

        # Check that the response renders the form page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/addcodepage.html')

        # Check that the form contains errors
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn('problem', form.errors)

    def test_add_code_problem_as_non_staff_user(self):
        # Log in as a non-staff user
        self.client.login(username='regular_user', password='password123')

        # Data for the valid form
        form_data = {
            'problem': 'Sample Problem',
            'description': 'Sample Description',
            'solution': 'Sample Solution',
            'status': 'Open',
            'language': 'Python'
        }

        # Send a POST request with valid form data
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to some restricted access page (403 Forbidden)
        self.assertEqual(response.status_code, 403)

        # Ensure that the problem was not saved in the database
        self.assertFalse(CodeProblem.objects.filter(problem='Sample Problem').exists())

    def test_add_code_problem_as_unauthenticated_user(self):
        # Data for the valid form
        form_data = {
            'problem': 'Sample Problem',
            'description': 'Sample Description',
            'solution': 'Sample Solution',
            'status': 'Open',
            'language': 'Python'
        }

        # Send a POST request to the view without logging in
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to the login page
        self.assertRedirects(response, f'{reverse("login")}?next={self.url}')

        # Ensure that the problem was not saved in the database
        self.assertFalse(CodeProblem.objects.filter(problem='Sample Problem').exists())

    def test_add_code_problem_get_request(self):
        # Send a GET request to the view
        response = self.client.get(self.url)

        # Check that the response renders the form page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/addcodepage.html')

        # Check that the form is in the context
        self.assertIsInstance(response.context['form'], CodeProblemForm)





class EditCommentTest(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(
            username='owner_user', password='ownerpassword'
        )
        self.other_user = User.objects.create_user(
            username='other_user', password='otherpassword'
        )

        # Create a sample CodeProblem instance
        self.problem = CodeProblem.objects.create(
            problem='Sample Problem',
            description='Sample Description',
            solution='Sample Solution',
            status='Open',
            language='Python'
        )

        # Create a comment instance
        self.comment = Comment.objects.create(
            user=self.owner,
            problem=self.problem,
            content='Original comment content'
        )

        # URL for editing the comment
        self.url = reverse('CBapp:edit_comment', kwargs={'comment_id': self.comment.id})

    def test_edit_comment_as_owner(self):
        # Log in as the owner of the comment
        self.client.login(username='owner_user', password='ownerpassword')

        # Data for the valid form
        form_data = {
            'content': 'Updated comment content'
        }

        # Send a POST request with valid form data
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to the code page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertRedirects(response, reverse('CBapp:codepage'))

        # Ensure that the comment was updated
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content')

    def test_edit_comment_as_other_user(self):
        # Log in as a different user
        self.client.login(username='other_user', password='otherpassword')

        # Data for the valid form
        form_data = {
            'content': 'Malicious content'
        }

        # Send a POST request with valid form data
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to the code page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertRedirects(response, reverse('CBapp:codepage'))

        # Ensure that the comment was not updated
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Original comment content')

    def test_edit_comment_not_logged_in(self):
        # Data for the valid form
        form_data = {
            'content': 'Updated comment content'
        }

        # Send a POST request with valid form data without logging in
        response = self.client.post(self.url, form_data)

        # Check that the response is a redirect to the login page
        self.assertRedirects(response, f'{reverse("login")}?next={self.url}')


class AddCommentViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a CodeProblem instance
        self.problem = CodeProblem.objects.create(
            problem='Sample Problem',
            description='Description of the problem',
            solution='Solution for the problem',
            status='active',
            language='python'
        )

        # Create a client instance
        self.client = Client()

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

    def test_add_comment_successful(self):
        # Prepare the comment data
        data = {'content': 'This is a test comment'}

        # Simulate a POST request to add a comment
        response = self.client.post(reverse('CBapp:add_comment', args=[self.problem.id]), data)

        # Assert that a comment was added
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'This is a test comment')
        self.assertEqual(Comment.objects.first().user, self.user)
        self.assertEqual(Comment.objects.first().problem, self.problem)

        # Assert redirection to the code page
        self.assertRedirects(response, reverse('CBapp:codepage'))

    def test_add_comment_invalid_form(self):
        # Prepare invalid comment data
        data = {'content': ''}  # Empty content should make the form invalid

        # Simulate a POST request to add a comment
        response = self.client.post(reverse('CBapp:add_comment', args=[self.problem.id]), data)

        # Assert that no comment was added
        self.assertEqual(Comment.objects.count(), 0)

        # Assert that the form is re-rendered with errors
        self.assertTemplateUsed(response, 'developer/codepage.html')
        form = response.context.get('form')
        self.assertIsInstance(form, CommentForm)
        self.assertTrue(form.errors)

    def test_add_comment_unauthenticated_user(self):
        # Log out the user
        self.client.logout()

        # Prepare the comment data
        data = {'content': 'This is a test comment'}

        # Simulate a POST request to add a comment
        response = self.client.post(reverse('CBapp:add_comment', args=[self.problem.id]), data)

        # Assert redirection to the login page
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("CBapp:add_comment", args=[self.problem.id])}')







class SendMessageTest(TestCase):
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_send_message_success(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

        # Create data for the message
        data = {
            'receiver': self.user.id,  # Assuming the receiver is the same user for testing
            'content': 'Hello, this is a test message.'
        }

        # Post data to the send_message view
        response = self.client.post(reverse('CBapp:send_message'), data)

        # Check if the message was successfully created
        self.assertEqual(response.status_code, 302)  # Redirects after a successful post
        self.assertEqual(Message.objects.count(), 1)  # Check if a message was created
        message = Message.objects.first()
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, 'Hello, this is a test message.')
        self.assertEqual(message.receiver, self.user)  # Assuming receiver is the same user
        self.assertAlmostEqual(message.timestamp, now(), delta=datetime.timedelta(seconds=1))

    def test_send_message_invalid_form(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

        # Create invalid data for the message (e.g., missing content)
        data = {
            'receiver': '',  # Missing receiver
            'content': ''    # Missing content
        }

        # Post data to the send_message view
        response = self.client.post(reverse('CBapp:send_message'), data)

        # Check if the form is rendered again due to invalid data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_page.html')
        self.assertContains(response, 'This field is required.')  # Checking form errors

        # Ensure no message was created
        self.assertEqual(Message.objects.count(), 0)


class ProblemDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.problem = CodeProblem.objects.create(
            problem="Sample Problem",
            description="This is a sample description.",
            solution="Official Solution",
            language="python",
        )
        self.url = reverse('CBapp:problem_detail', args=[self.problem.id])

    def test_get_problem_detail(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/problem_detail.html')
        self.assertIn('problem', response.context)
        self.assertIn('user_solutions', response.context)
        self.assertIn('other_solutions', response.context)
        self.assertIn('official_solution', response.context)
        self.assertIn('solution_form', response.context)

    @patch('CBapp.views.analyze_code')
    def test_post_solution_valid_data(self, mock_analyze_code):
        mock_analyze_code.return_value = "AI-generated feedback"

        self.client.login(username='testuser', password='testpass')
        data = {
            'content': 'Sample solution content'
        }
        response = self.client.post(self.url, data)

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

        # Check that the solution was saved in the database
        solution = Solution.objects.get(problem=self.problem, user=self.user)
        self.assertEqual(solution.content, 'Sample solution content')
        self.assertEqual(solution.feedback, "AI-generated feedback")
        self.assertEqual(solution.problem, self.problem)
        self.assertEqual(solution.user, self.user)

        # Check that the analyze_code function was called with correct arguments
        mock_analyze_code.assert_called_once_with('Sample solution content', self.problem.description,
                                                  self.problem.language)

    def test_post_solution_invalid_data(self):
        self.client.login(username='testuser', password='testpass')

        data = {'content': ''}  # Invalid data (empty content)
        response = self.client.post(self.url, data)

        # The page should re-render with the form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/problem_detail.html')
        self.assertContains(response, 'This field is required.')
        self.assertEqual(Solution.objects.count(), 0)  # No solution should be saved

class CodepageViewTest(TestCase):

    def setUp(self):
        # Create test users and groups
        self.developer_group = Group.objects.create(name='Developer')
        self.student_group = Group.objects.create(name='Student')

        self.developer_user = User.objects.create_user(username='devuser', password='testpass')
        self.student_user = User.objects.create_user(username='stuuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='testpass', is_staff=True)

        self.developer_user.groups.add(self.developer_group)
        self.student_user.groups.add(self.student_group)

        # Create test problems
        self.problem1 = CodeProblem.objects.create(
            problem='Problem 1', description='Description 1', solution='Solution 1', status='accepted',
            language='Python'
        )
        self.problem2 = CodeProblem.objects.create(
            problem='Problem 2', description='Description 2', solution='Solution 2', status='pending',
            language='JavaScript'
        )

        self.url = reverse('CBapp:codepage')

    def test_get_codepage_view(self):
        self.client.login(username='devuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/codepage.html')

        # Check if context contains the necessary data
        self.assertIn('is_developer', response.context)
        self.assertIn('is_student', response.context)
        self.assertIn('code_problems', response.context)
        self.assertIn('accepted_problems', response.context)
        self.assertIn('form', response.context)
        self.assertIn('is_staff', response.context)
        self.assertIn('problem_comments', response.context)
        self.assertIn('comment_form', response.context)

        # Check the problems in the context
        problems = response.context['code_problems']
        self.assertIn(self.problem1, problems)
        self.assertIn(self.problem2, problems)

        # Check markdown conversion
        self.assertEqual(
            response.context['code_problems'].get(id=self.problem1.id).description,
            mark_safe(markdown.markdown(self.problem1.description, extensions=['fenced_code']))
        )

    @patch('CBapp.views.CommentForm')
    def test_post_comment_success(self, MockCommentForm):
        mock_form = MagicMock()
        MockCommentForm.return_value = mock_form
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = None

        self.client.login(username='stuuser', password='testpass')
        data = {
            'problem_id': self.problem1.id,
            'content': 'This is a comment'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)  # Should redirect after successful comment
        self.assertRedirects(response, self.url)

        # Check that the comment was saved
        self.assertTrue(
            Comment.objects.filter(problem=self.problem1, user=self.student_user, content='This is a comment').exists())
        mock_form.save.assert_called_once()

    @patch('CBapp.views.CommentForm')
    def test_post_comment_invalid_data(self, MockCommentForm):
        mock_form = MagicMock()
        MockCommentForm.return_value = mock_form
        mock_form.is_valid.return_value = False

        self.client.login(username='stuuser', password='testpass')
        data = {
            'problem_id': self.problem1.id,
            'content': ''  # Invalid comment content
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)  # Should re-render the form
        self.assertTemplateUsed(response, 'developer/codepage.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['comment_form'].is_valid())

        # Ensure no new comments were added
        self.assertFalse(Comment.objects.filter(problem=self.problem1, user=self.student_user).exists())
        mock_form.save.assert_not_called()





class EditSolutionViewTest(TestCase):

    def setUp(self):
        # Create a test user and problem
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.problem = CodeProblem.objects.create(
            problem='Test Problem',
            description='Test Description',
            solution='Test Solution',
            status='accepted',
            language='Python'
        )
        self.url = reverse('CBapp:edit_solution', args=[self.problem.id])

    def test_get_edit_solution_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'developer/edit_solution.html')

        form = response.context['form']
        problem = response.context['problem']

        self.assertIsInstance(form, CodeProblemForm)
        self.assertEqual(problem, self.problem)
        self.assertEqual(form.initial['problem'], self.problem.problem)
        self.assertEqual(form.initial['description'], self.problem.description)
        self.assertEqual(form.initial['solution'], self.problem.solution)

    def test_post_edit_solution_success(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'problem': 'Updated Problem',
            'description': 'Updated Description',
            'solution': 'Updated Solution',
            'status': 'accepted',
            'language': 'Python'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.assertRedirects(response, reverse('CBapp:codepage'))

        # Refresh problem instance from the database
        updated_problem = CodeProblem.objects.get(id=self.problem.id)

        self.assertEqual(updated_problem.problem, 'Updated Problem')
        self.assertEqual(updated_problem.description, 'Updated Description')
        self.assertEqual(updated_problem.solution, 'Updated Solution')

    def test_post_edit_solution_invalid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'problem': '',  # Invalid data
            'description': '',
            'solution': '',
            'status': 'accepted',
            'language': 'Python'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)  # Should re-render the form
        self.assertTemplateUsed(response, 'developer/edit_solution.html')

        form = response.context['form']
        self.assertFalse(form.is_valid())

        # Check that the problem was not updated
        unchanged_problem = CodeProblem.objects.get(id=self.problem.id)
        self.assertEqual(unchanged_problem.problem, 'Test Problem')
        self.assertEqual(unchanged_problem.description, 'Test Description')
        self.assertEqual(unchanged_problem.solution, 'Test Solution')


if __name__ == '__main__':
    unittest.main()

