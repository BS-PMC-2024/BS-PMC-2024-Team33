from django.contrib import admin

from .models import CodeProblem, Comment, Message, Solution, CommentReply
from .models import Tutorial

admin.site.register(CodeProblem)
admin.site.register(Tutorial)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Solution)
admin.site.register(CommentReply)