from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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

        # Uncomment the following lines if upload_file is required for developers
        # if role == 'developer' and not upload_file:
        #     self.add_error('upload_file', 'This field is required for developers.')

        return cleaned_data


class CustomUserEditForm(UserChangeForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user