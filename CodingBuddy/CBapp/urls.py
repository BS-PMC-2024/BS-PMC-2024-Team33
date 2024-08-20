from django.urls import path

from . import views
from .controller import approveCB_views
from .controller import tutorials_views
from .views import chat_page

app_name = 'CBapp'

urlpatterns = [
    path('aboutus/', views.aboutus, name='aboutus'),
    path('codepage/', views.codepage, name='codepage'),
    path('problem/<int:id>/', views.problem_detail, name='problem_detail'),
    path('addcodepage/', views.add_code_problem, name='add_code_problem'),
    path('edit_solution/<int:problem_id>/', views.edit_solution, name='edit_solution'),
    path('delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('student_problem/', views.view_problems_for_student, name='student_problem'),
    path('tutorials/', tutorials_views.tutorial_list_developer, name='tutorial_list_developer'),
    path('developer/tutorials/add/', tutorials_views.add_tutorial, name='add_tutorial'),
    path('developer/tutorials/edit/<int:tutorial_id>/', tutorials_views.edit_tutorial, name='edit_tutorial'),
    path('admin/CBstatus/', approveCB_views.admin_problem_list, name='CBstatus'),
    path('admin/problems/<int:problem_id>/update/', approveCB_views.admin_update_problem, name='admin_update_problem'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('student/tutorials/', tutorials_views.tutorial_list_student, name='student_tutorials'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('chat/', chat_page, name='chat_page'),
    path('check_new_messages/', views.check_new_messages, name='check_new_messages'),
    path('add_comment/<int:problem_id>/', views.add_comment, name='add_comment'),  # Add this line
    path('send_message/', views.send_message, name='send_message'),  # Add this line
    path('add_comment_reply/<int:comment_id>/', views.add_comment_reply, name='add_comment_reply'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),

]
