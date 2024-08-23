from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Tutorial
from ..forms import TutorialDeveloperForm


@login_required
def tutorial_list_developer(request):
    user = request.user
    is_developer = user.groups.filter(name='Developer').exists()
    is_student = user.groups.filter(name='Student').exists()
    selected_language = request.GET.get('language', '')

    # Filter the tutorials by the selected language if provided
    if selected_language:
        tutorials = Tutorial.objects.filter(language=selected_language)
    else:
        tutorials = Tutorial.objects.all()

    # Retrieve distinct languages for the filter dropdown
    languages = Tutorial.objects.values_list('language', flat=True).distinct()

    is_staff = user.is_staff

    context = {
        'is_developer': is_developer,
        'is_student': is_student,
        'tutorials': tutorials,
        'is_staff': is_staff,
        'languages': languages,
        'selected_language': selected_language,
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


def tutorial_list_student(request):
    selected_language = request.GET.get('language', '')

    if selected_language:
        tutorials = Tutorial.objects.filter(language=selected_language)
    else:
        tutorials = Tutorial.objects.all()

    languages = Tutorial.objects.values_list('language', flat=True).distinct()

    context = {
        'tutorials': tutorials,
        'languages': languages,
        'selected_language': selected_language,
    }
    return render(request, 'student/tutorial_list.html', context)