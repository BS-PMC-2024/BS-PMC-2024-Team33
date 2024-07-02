from django import forms
from .models import CodeProblem

class CodeProblemForm(forms.ModelForm):
    class Meta:
        model = CodeProblem
        fields = ['problem', 'description','solution']
