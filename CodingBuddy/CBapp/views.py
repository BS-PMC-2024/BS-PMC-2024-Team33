import datetime

import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from .forms import CodeProblemForm, MessageForm, ProblemFilterForm, CommentForm, TutorialDeveloperForm, SolutionForm, \
    CommentReplyForm
from .models import CodeProblem, Comment, Message, Tutorial, Solution, CommentReply


def aboutus(request):
    return render(request, 'aboutus.html')


@require_http_methods(["POST"])
def delete_problem(request, problem_id):
    problem = get_object_or_404(CodeProblem, pk=problem_id)
    if request.user.is_authenticated and request.user.is_staff:
        problem.delete()
        return JsonResponse({'message': 'Problem deleted successfully.'}, status=204)
    return JsonResponse({'error': 'Unauthorized'}, status=403)


def add_code_problem(request):
    if request.method == 'POST':
        form = CodeProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CBapp:codepage')
    else:
        form = CodeProblemForm()
    return render(request, 'developer/addcodepage.html', {'form': form})


@login_required
def codepage(request):
    user = request.user
    is_developer = user.groups.filter(name='Developer').exists()
    is_student = user.groups.filter(name='Student').exists()
    is_staff = user.is_staff

    form = ProblemFilterForm(request.GET or None)
    code_problems = CodeProblem.objects.all()
    accepted_problems = CodeProblem.objects.filter(status='accepted')

    if form.is_valid():
        language = form.cleaned_data.get('language')
        if language:
            code_problems = code_problems.filter(language__icontains=language)
            accepted_problems = accepted_problems.filter(language__icontains=language)

    comment_form = CommentForm()
    reply_form = CommentReplyForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            problem_id = request.POST.get('problem_id')
            problem = CodeProblem.objects.get(id=problem_id)
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.problem = problem
            comment.save()
            return redirect('CBapp:codepage')

        reply_form = CommentReplyForm(request.POST)
        if reply_form.is_valid():
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            reply = reply_form.save(commit=False)
            reply.user = user
            reply.comment = comment
            reply.save()
            return redirect('CBapp:codepage')

    problem_comments = {problem.id: problem.comments.all() for problem in code_problems}

    for problem in code_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    for problem in accepted_problems:
        problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
        problem.solution = mark_safe(markdown.markdown(problem.solution, extensions=['fenced_code']))

    context = {'is_developer': is_developer, 'is_student': is_student, 'code_problems': code_problems,
        'accepted_problems': accepted_problems, 'form': form, 'is_staff': is_staff,
        'problem_comments': problem_comments, 'comment_form': comment_form, 'reply_form': reply_form, }
    return render(request, 'developer/codepage.html', context)


@login_required
def problem_detail(request, id):
    problem = get_object_or_404(CodeProblem, id=id)
    user_solutions = Solution.objects.filter(problem=problem, user=request.user)
    other_solutions = Solution.objects.filter(problem=problem).exclude(user=request.user)
    official_solution = problem.solution

    solution_form = SolutionForm()

    if request.method == 'POST':
        solution_form = SolutionForm(request.POST)
        if solution_form.is_valid():
            solution = solution_form.save(commit=False)
            solution.user = request.user
            solution.problem = problem
            # Generate AI feedback
            feedback = analyze_code(solution.content, problem.description, problem.language)
            solution.feedback = feedback
            solution.save()
            return redirect('CBapp:problem_detail', id=id)

    problem.description = mark_safe(markdown.markdown(problem.description, extensions=['fenced_code']))
    official_solution = mark_safe(markdown.markdown(official_solution, extensions=['fenced_code']))

    context = {'problem': problem, 'user_solutions': user_solutions, 'other_solutions': other_solutions,
        'official_solution': official_solution, 'solution_form': solution_form, }
    return render(request, 'developer/problem_detail.html', context)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return redirect('CBapp:codepage')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('CBapp:codepage')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'developer/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def edit_solution(request, problem_id):
    problem = get_object_or_404(CodeProblem, pk=problem_id)
    if request.method == 'POST':
        form = CodeProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('CBapp:codepage')
    else:
        form = CodeProblemForm(instance=problem)
    return render(request, 'developer/edit_solution.html', {'form': form, 'problem': problem})


@login_required
def view_problems_for_student(request):
    accepted_problems = CodeProblem.objects.filter(status='accepted')
    form = ProblemFilterForm(request.GET or None)

    if form.is_valid():
        language = form.cleaned_data.get('language')
        if language:
            accepted_problems = accepted_problems.filter(language=language)

    return render(request, 'developer/codepage.html', {'accepted_problems': accepted_problems, 'form': form})




@login_required
def add_tutorial(request):
    if request.method == 'POST':
        form = TutorialDeveloperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CBapp:tutorial_list_developer')
    else:
        form = TutorialDeveloperForm()
    return render(request, 'developer/add_tutorial.html', {'form': form})


@login_required
def edit_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    if request.method == 'POST':
        form = TutorialDeveloperForm(request.POST, instance=tutorial)
        if form.is_valid():
            form.save()
            return redirect('CBapp:tutorial_list_developer')
    else:
        form = TutorialDeveloperForm(instance=tutorial)
    return render(request, 'developer/edit_tutorial.html', {'form': form})


@login_required
def chat_page(request):
    developers_group = Group.objects.get(name='Developer')
    developers = User.objects.filter(groups=developers_group)
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('timestamp')
    new_messages = messages.filter(receiver=request.user, read=False).exists()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.timestamp = datetime.datetime.now()
            message.save()
            return redirect('CBapp:chat_page')
    else:
        form = MessageForm()

    messages.filter(receiver=request.user, read=False).update(read=True)

    if request.user in developers:
        form.fields['receiver'].queryset = User.objects.filter(groups__name='Developer').union(
            User.objects.filter(groups__name='Student'))
    else:
        form.fields['receiver'].queryset = User.objects.filter(groups__name='Developer')

    return render(request, 'chat_page.html',
                  {'messages': messages, 'form': form, 'user_has_new_messages': new_messages})


@login_required
def check_new_messages(request):
    if request.user.is_authenticated:
        new_messages = Message.objects.filter(receiver=request.user, read=False).exists()
        return JsonResponse({'new_messages': new_messages})
    return JsonResponse({'new_messages': False})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the comment's owner or an admin
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully.'}, status=204)

    return JsonResponse({'error': 'You do not have permission to delete this comment.'}, status=403)


@login_required
@require_http_methods(["POST"])
def add_comment(request, problem_id):
    problem = get_object_or_404(CodeProblem, id=problem_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.problem = problem
        comment.save()
        return redirect('CBapp:codepage')
    return render(request, 'developer/codepage.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def add_comment_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect('CBapp:codepage')  # Redirect back to the codepage or relevant page

    return redirect('CBapp:codepage')


def delete_reply(request, reply_id):
    reply = get_object_or_404(CommentReply, id=reply_id)

    # Check if the user is an admin and the owner of the reply
    if request.user.is_staff and request.user == reply.user:
        if request.method == 'POST':
            reply.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseForbidden("You do not have permission to delete this reply.")
    else:
        return HttpResponseForbidden("You do not have permission to delete this reply.")


@login_required
@require_http_methods(["POST"])
def send_message(request):
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.timestamp = datetime.datetime.now()
        message.save()
        return redirect('CBapp:chat_page')
    return render(request, 'chat_page.html', {'form': form})


import openai
from django.conf import settings

# Ensure you have your OpenAI API key stored in Django settings
openai.api_key = settings.OPENAI_API_KEY

import openai
from django.conf import settings


def analyze_code(code, issue, language):
    try:

        openai.api_key = settings.OPENAI_API_KEY
        content = f"""
                Please check if the following code addresses the issue described below:

                Issue:
                {issue}

                Language:
                {language}

                Code:
                {code}

                Additionally, analyze the code and provide detailed feedback on its correctness, efficiency, and potential improvements only if it's related to the issue, otherwise provide solution to the issue.
                """
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert code analyzer."},
                {"role": "user", "content": content}])

        # Extracting the response content
        feedback = response['choices'][0]['message']['content']
        print(feedback)

        # Extract and return the feedback
        return feedback

    except Exception as e:
        # Handle exceptions
        return f"Error generating feedback: {str(e)}"
