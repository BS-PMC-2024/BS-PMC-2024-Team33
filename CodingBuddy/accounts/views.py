"""
Views for user account management, including sign-up and approval processes.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from .forms import CustomUserCreationForm, CustomUserEditForm


def signup_view(request):
    """
    Handle the sign-up process for new users.

    This view allows users to sign up by providing the necessary details.
    Depending on the role selected (student or developer), the user will
    either be automatically logged in (for students) or require admin
    approval (for developers).

    If the form is not valid, it will re-render the signup page with error
    messages.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered signup page or a redirect to the appropriate
        page after successful signup.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')

            if role == 'developer':
                user.is_active = False  # Require admin approval for developers
            user.save()

            # Add user to the appropriate group
            if role == 'student':
                group = Group.objects.get(name='Student')
                group.user_set.add(user)
                login(request, user)
                return redirect('home')
            if role == 'developer':
                group = Group.objects.get(name='Developer')
                group.user_set.add(user)
                # Redirect to a signup success page for developers
                return redirect('signup_success')
        else:
            print(form.errors)
            # If form is not valid, it will be rendered again with error messages
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def signup_success(request):
    """
    Render the sign-up success page for developers.

    This view is displayed after a developer successfully signs up, indicating
    that their account requires admin approval before it can be activated.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered signup success page.
    """
    return render(request, 'registration/signup_success.html')


@method_decorator(staff_member_required, name='dispatch')
class InactiveUserListView(ListView):
    """
    View to list inactive users for admin approval.

    This view lists all users who have signed up but are currently inactive,
    typically awaiting admin approval. Only staff members can access this view.

    Attributes:
        model (User): The model to query for the list of users.
        template_name (str): The template to use for rendering the user list.
        context_object_name (str): The context variable name for the user list.
    """

    model = User
    template_name = 'admin/unapproved_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        """
        Override the default queryset to filter for inactive users.

        Returns:
            QuerySet: The queryset of inactive users.
        """
        return User.objects.filter(is_active=False)


@method_decorator(staff_member_required, name='dispatch')
class ApproveUsersView(View):
    """
    View to approve inactive users.

    This view allows staff members to activate user accounts that are currently
    inactive. The user IDs are provided via POST request, and the users are
    activated if they belong to the Developer group.

    Methods:
        post: Handles the approval of inactive users.
    """

    def post(self, request):
        """
        Activate selected users based on their IDs.

        Args:
            request (HttpRequest): The incoming HTTP request containing the user IDs.

        Returns:
            HttpResponse: A redirect to the unapproved users page after activation.
        """
        user_ids = request.POST.getlist('user_ids')
        developer_group = Group.objects.get(name='Developer')
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            user.is_active = True
            user.save()
            if developer_group in user.groups.all():
                developer_group.user_set.add(user)
        return redirect('unapproved_users')


@login_required
def profile_view(request):
    """
    Display and handle profile editing for the logged-in user.

    This view allows the logged-in user to view and edit their profile details.
    If the form is valid upon submission, the user's details are updated.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered profile page with the form or a redirect to
        the home page after successful profile update.
    """
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})
