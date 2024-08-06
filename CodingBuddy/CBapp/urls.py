from django.urls import path
from . import views
from .controller import tutorials_views
from .controller import approveCB_views

app_name = 'CBapp'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('codepage/', views.codepage, name='codepage'),
    path('addcodepage/', views.addcodepage, name='addcodepage'),
    path('addcodepage', views.add_code_problem, name='add_code_problem'),
    path('edit_solution/<int:problem_id>/', views.edit_solution, name='edit_solution'),
    path('delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('student_problem', views.ViewProblmesForStudent, name='student_problem'),
    path('tutorials/', tutorials_views.tutorial_list_developer, name='tutorial_list_developer'),
    path('developer/tutorials/add/', tutorials_views.add_tutorial, name='add_tutorial'),
    path('developer/tutorials/edit/<int:tutorial_id>/', tutorials_views.edit_tutorial, name='edit_tutorial'),
    path('admin/CBstatus/', approveCB_views.admin_problem_list, name='CBstatus'),
    path('admin/problems/<int:problem_id>/update/', approveCB_views.admin_update_problem, name='admin_update_problem'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('student/tutorials/', tutorials_views.tutorial_list_student, name='student_tutorials'),

]
