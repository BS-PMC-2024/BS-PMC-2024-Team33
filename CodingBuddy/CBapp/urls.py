from django.urls import path
from . import views


app_name = 'CBapp'


urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('codepage/', views.codepage, name='codepage'),
    path('addcodepage/', views.addcodepage, name='addcodepage'),
    path('addcodepage', views.add_code_problem, name='add_code_problem'),
    path('edit_solution/<int:problem_id>/', views.edit_solution, name='edit_solution'),
    path('delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('student_problem', views.ViewProblmesForStudent, name='student_problem'),


    # Add more paths as needed for your CBapp views
]
