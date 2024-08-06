from django import forms

from .models import CodeProblem, Comment
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

class AdminCodeProblemForm(forms.ModelForm):
    class Meta:
        model = CodeProblem
        fields = ['status']

from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Send to",
        required=True,
        widget=forms.Select
    )

    class Meta:
        model = Message
        fields = ['receiver', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']