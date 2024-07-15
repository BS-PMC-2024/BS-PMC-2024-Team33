from django.shortcuts import render
from ..models import Tutorial

def tutorial_list_developer(request):
    tutorials = Tutorial.objects.all()
    return render(request, 'developer/tutorial_list.html', {'tutorials': tutorials})

