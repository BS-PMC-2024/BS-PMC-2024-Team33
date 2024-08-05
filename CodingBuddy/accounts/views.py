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
                return redirect('signup_success')  # Redirect to a signup success page for developers
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
    """
    return render(request, 'registration/signup_success.html')

@method_decorator(staff_member_required, name='dispatch')
class InactiveUserListView(ListView):
    """
    View to list inactive users for admin approval.
    """
    model = User
    template_name = 'admin/unapproved_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        """
        Override the default queryset to filter for inactive users.
        """
        return User.objects.filter(is_active=False)

@method_decorator(staff_member_required, name='dispatch')
class ApproveUsersView(View):
    """
    View to approve inactive users.
    """
    def post(self, request, *args, **kwargs):
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
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})
