from django import forms
from .models import CodeProblem

class CodeProblemForm(forms.ModelForm):
    class Meta:
        model = CodeProblem
        fields = ['problem', 'description','solution','language']

class ProblemFilterForm(forms.Form):
    language = forms.CharField(max_length=50, required=False)