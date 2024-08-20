from django import forms
from .models import CodeProblem, Comment, Solution, Tutorial, CommentReply


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

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['content']

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'placeholder': 'Enter your solution here...'}),
        }
