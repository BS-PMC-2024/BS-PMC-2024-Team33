from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CodeProblemForm
from .forms import ProblemFilterForm
from .models import CodeProblem
from django.http import JsonResponse
import markdown
from django.utils.safestring import mark_safe

# Assuming `code_problems` is a global variable for simplicity
code_problems = []

def homepage(request):
    return render(request, 'developer/homepage.html')


def delete_problem(request, problem_id):
    problem = get_object_or_404(CodeProblem, pk=problem_id)
    if request.method == 'POST':
        problem.delete()
        return JsonResponse({'message': 'Problem deleted successfully.'}, status=204)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
def addcodepage(request):
    if request.method == 'POST':
        problem = request.POST.get('problem')
        code_problems.append(problem)
        return redirect('codepage')  # Redirect to the codepage view
    return render(request, 'developer/addcodepage.html')
def add_code_problem(request):
    if request.method == 'POST':
        form = CodeProblemForm(request.POST)
        if form.is_valid():
            form.save()  # This will save 'problem' and 'description' to the database
            return redirect('CBapp:codepage')  # Redirect after successful submission
    else:
        form = CodeProblemForm()

    return render(request, 'developer/addcodepage.html', {'form': form})
# In your views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def codepage(request):
    user = request.user
    is_developer = user.groups.filter(name='Developer').exists()
    is_student = user.groups.filter(name='Student').exists()

    code_problems = CodeProblem.objects.all()
    accepted_problems = CodeProblem.objects.filter(status='accepted')

    for problem in code_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    for problem in accepted_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    context = {
        'is_developer': is_developer,
        'is_student': is_student,
        'code_problems': code_problems,
        'accepted_problems': accepted_problems,
    }
    return render(request, 'developer/codepage.html', context)
def edit_solution(request, problem_id):
    problem = get_object_or_404(CodeProblem, pk=problem_id)

    if request.method == 'POST':
        form = CodeProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            # Redirect or display success message
            return redirect('CBapp:codepage')  # Redirect to a view where code problems are listed
    else:
        form = CodeProblemForm(instance=problem)

    return render(request, 'developer/edit_solution.html', {'form': form, 'problem': problem})

def ViewProblmesForStudent(request):
    accepted_problems = CodeProblem.objects.filter(status='accepted')
    form = ProblemFilterForm(request.GET or None)

    if form.is_valid():
        language = form.cleaned_data.get('language')
        if language:
            accepted_problems = accepted_problems.filter(language=language)

    return render(request, 'student/Showing_Problems.html', {'accepted_problems': accepted_problems, 'form': form})