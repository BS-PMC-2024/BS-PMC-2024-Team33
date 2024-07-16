from django.db import models

class CodeProblem(models.Model):
    problem = models.CharField(max_length=100)
    description = models.TextField()
    solution = models.TextField()
    status = models.CharField(max_length=20, default="not accepted")
    language = models.CharField(max_length=50)


    def __str__(self):
        return self.problem

class Tutorial(models.Model):
    LANGUAGE_CHOICES = [
        ('c', 'C'),
        ('python', 'Python'),
        ('java', 'Java'),
        # Add more choices as needed
    ]

    youtube_link = models.URLField(blank=True, null=True)
    medium_link = models.URLField(blank=True, null=True)
    wikipedia_link = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return f"Tutorial ({self.language})"


