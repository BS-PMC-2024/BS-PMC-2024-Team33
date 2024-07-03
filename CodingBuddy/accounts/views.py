from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group  # Ensure this line is present
from django.views import View

from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm

def signup_view(request):
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
            elif role == 'developer':
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
    return render(request, 'registration/signup_success.html')

@method_decorator(staff_member_required, name='dispatch')
class InactiveUserListView(ListView):
    model = User
    template_name = 'admin/unapproved_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_active=False)

@method_decorator(staff_member_required, name='dispatch')
class ApproveUsersView(View):
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
    return render(request, 'profile.html')