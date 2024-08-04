from django import forms
from .models import CodeProblem
from .models import Tutorial
from .models import CodeProblem, Comment
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

class AdminCodeProblemForm(forms.ModelForm):
    class Meta:
        model = CodeProblem
        fields = ['status']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']