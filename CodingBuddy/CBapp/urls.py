from django.urls import path
from . import views
from .controller import tutorials_views
app_name = 'CBapp'


urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('codepage/', views.codepage, name='codepage'),
    path('addcodepage/', views.addcodepage, name='addcodepage'),
    path('addcodepage', views.add_code_problem, name='add_code_problem'),
    path('edit_solution/<int:problem_id>/', views.edit_solution, name='edit_solution'),
    path('delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('student_problem', views.ViewProblmesForStudent, name='student_problem'),
    path('developer/tutorials/', tutorials_views.tutorial_list_developer, name='tutorial_list_developer'),
    path('developer/tutorials/add/', tutorials_views.add_tutorial, name='add_tutorial'),
    path('developer/tutorials/edit/<int:tutorial_id>/', tutorials_views.edit_tutorial, name='edit_tutorial'),
   ]
