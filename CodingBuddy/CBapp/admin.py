from django.contrib import admin

from .models import CodeProblem, Comment
from .models import Tutorial

admin.site.register(CodeProblem)
admin.site.register(Tutorial)
admin.site.register(Comment)
