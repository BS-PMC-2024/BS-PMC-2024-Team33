from django import forms
from .models import CodeProblem
from .models import Tutorial

class CodeProblemForm(forms.ModelForm):
    class Meta:
        model = CodeProblem
        fields = ['problem', 'description','solution','language']

class ProblemFilterForm(forms.Form):
    language = forms.CharField(max_length=50, required=False)

class TutorialDeveloperForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['youtube_link', 'medium_link', 'wikipedia_link', 'language']