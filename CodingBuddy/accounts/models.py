from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('developer', 'Developer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    upload_file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.user.username
