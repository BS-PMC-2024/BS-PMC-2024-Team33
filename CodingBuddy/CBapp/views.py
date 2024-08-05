from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CodeProblemForm
from .forms import ProblemFilterForm
from .models import CodeProblem
from django.http import JsonResponse
import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import CodeProblem, Comment
from .forms import ProblemFilterForm, CommentForm
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
        CodeProblem.append(problem)
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


@login_required
def codepage(request):
    # Get the current user
    user = request.user

    # Check user roles
    is_developer = user.groups.filter(name='Developer').exists()
    is_student = user.groups.filter(name='Student').exists()
    is_staff = user.is_staff

    # Initialize the form for filtering code problems based on language
    form = ProblemFilterForm(request.GET or None)

    # Query all code problems and accepted problems
    code_problems = CodeProblem.objects.all()
    accepted_problems = CodeProblem.objects.filter(status='accepted')

    # If the form is valid and a language is selected, filter the code problems
    if form.is_valid():
        language = form.cleaned_data.get('language')
        if language:
            code_problems = code_problems.filter(language__icontains=language)
            accepted_problems = accepted_problems.filter(language__icontains=language)

    # Initialize comment form
    comment_form = CommentForm()

    # Process new comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            problem_id = request.POST.get('problem_id')
            problem = CodeProblem.objects.get(id=problem_id)
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.problem = problem
            comment.save()
            return redirect('CBapp:codepage')  # Redirect to avoid re-submission on refresh

    # Retrieve comments for code problems
    problem_comments = {problem.id: problem.comments.all() for problem in code_problems}

    # Process and mark safe markdown content for code problems
    for problem in code_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    # Process and mark safe markdown content for accepted problems
    for problem in accepted_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    # Prepare context for rendering the template
    context = {
        'is_developer': is_developer,
        'is_student': is_student,
        'code_problems': code_problems,
        'accepted_problems': accepted_problems,
        'form': form,
        'is_staff': is_staff,
        'problem_comments': problem_comments,  # Include comments for code problems
        'comment_form': comment_form,  # Form for adding comments
    }

    # Render the 'codepage.html' template with the context data
    return render(request, 'developer/codepage.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return redirect('CBapp:codepage')  # Redirect if the user is not the owner of the comment

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('CBapp:codepage')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'developer/edit_comment.html', {'form': form, 'comment': comment})


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
    return render(request, 'developer/codepage.html', {'accepted_problems': accepted_problems, 'form': form})

from .models import Tutorial
from .forms import TutorialDeveloperForm

def tutorial_list_developer(request):
    user = request.user
    is_developer = user.groups.filter(name='Developer').exists()
    is_staff = user.is_staff
    tutorials = Tutorial.objects.all()
    context = {
        'is_developer': is_developer,
        'is_staff': is_staff,
        'tutorials': tutorials
    }
    return render(request, 'developer/tutorial_list.html', context)

def add_tutorial(request):
    if request.method == 'POST':
        form = TutorialDeveloperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CBapp:tutorial_list_developer')
    else:
        form = TutorialDeveloperForm()
    return render(request, 'developer/add_tutorial.html', {'form': form})

def edit_tutorial(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    if request.method == 'POST':
        form = TutorialDeveloperForm(request.POST, instance=tutorial)
        if form.is_valid():
            form.save()
            return redirect('CBapp:tutorial_list_developer')
    else:
        form = TutorialDeveloperForm(instance=tutorial)
    return render(request, 'developer/edit_tutorial.html', {'form': form})
