
from django.shortcuts import render, redirect
from ..models import Tutorial
from ..forms import TutorialDeveloperForm

def tutorial_list_developer(request):
    tutorials = Tutorial.objects.all()
    return render(request, 'developer/tutorial_list.html', {'tutorials': tutorials})

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
