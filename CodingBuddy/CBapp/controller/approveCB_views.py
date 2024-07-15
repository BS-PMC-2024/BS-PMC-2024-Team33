from django.shortcuts import render, redirect, get_object_or_404
from ..models import CodeProblem
from ..forms import AdminCodeProblemForm

def admin_problem_list(request):
    problems = CodeProblem.objects.all()
    return render(request, 'admin/CBstatus.html', {'problems': problems})

def admin_update_problem(request, problem_id):
    problem = get_object_or_404(CodeProblem, id=problem_id)
    if request.method == 'POST':
        form = AdminCodeProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('CBapp:CBstatus')
    else:
        form = AdminCodeProblemForm(instance=problem)
    return render(request, 'admin_update_problem.html', {'form': form, 'problem': problem})
