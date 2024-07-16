from django.shortcuts import render, redirect
from ..models import Tutorial
from ..forms import TutorialDeveloperForm

def tutorial_list_developer(request):
    user = request.user
    is_developer = user.groups.filter(name='Developer').exists()
    is_student = user.groups.filter(name='Student').exists()
    is_staff = user.is_staff
    tutorials = Tutorial.objects.all()
    context = {
        'is_developer': is_developer,
        'is_student': is_student,
        'tutorials': tutorials,
        'is_staff': is_staff,
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
