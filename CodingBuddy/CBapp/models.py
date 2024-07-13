from django.db import models

class CodeProblem(models.Model):
    problem = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    solution = models.CharField(max_length=1000, default="")
    status = models.CharField(max_length=20, default="not accepted")
    language = models.CharField(max_length=50)


    def __str__(self):
        return self.problem
