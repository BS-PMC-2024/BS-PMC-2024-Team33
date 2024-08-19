import datetime
import unittest

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from .models import CodeProblem, Tutorial, Comment, Message


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
        tutorial = Tutorial.objects.create(youtube_link='Sample Tutorial', medium_link='Tutorial Content',wikipedia_link='las;kd', language='Python')
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
        self.assertEqual(response.context['form'].instance, self.tutorial)

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
        self.assertFormError(response, 'form', 'language', 'This field is required.')

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


from django.test import TestCase, Client
from django.urls import reverse
from CBapp.models import Tutorial


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


if __name__ == '__main__':
    unittest.main()
