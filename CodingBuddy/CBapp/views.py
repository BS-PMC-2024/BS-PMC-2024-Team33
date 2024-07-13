from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CodeProblemForm
from .forms import ProblemFilterForm
from .models import CodeProblem
from django.http import JsonResponse

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
def codepage(request):
    code_problems = CodeProblem.objects.all()
    return render(request, 'developer/codepage.html', {'code_problems': code_problems})
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