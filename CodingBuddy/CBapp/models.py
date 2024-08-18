from django.contrib.auth.models import User
from django.db import models


class CodeProblem(models.Model):
    problem = models.CharField(max_length=255)
    description = models.TextField()
    solution = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])
    language = models.CharField(max_length=50)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(CodeProblem, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()
    read = models.BooleanField(default=False)

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


class CC(models.Model):
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

class Solution(models.Model):
    problem = models.ForeignKey(CodeProblem, on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution by {self.user.username} for {self.problem.problem}"