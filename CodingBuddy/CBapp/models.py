from django.db import models

class CodeProblem(models.Model):
    problem = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    solution = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.problem
