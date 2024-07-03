from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('developer', 'Developer'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    upload_file = forms.FileField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'upload_file')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        upload_file = cleaned_data.get('upload_file')

        #if role == 'developer' and not upload_file:
         #   self.add_error('upload_file', 'This field is required for developers.')

        return cleaned_data
