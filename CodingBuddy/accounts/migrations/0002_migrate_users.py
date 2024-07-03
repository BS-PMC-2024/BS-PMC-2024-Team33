from django.db import migrations, transaction
from django.contrib.auth import get_user_model

def forwards(apps, schema_editor):
    # Use the historical model from the apps parameter to access the original auth.User model
    User = apps.get_model('auth', 'User')
    CustomUser = get_user_model()

    with transaction.atomic():
        for user in User.objects.all():
            custom_user = CustomUser(
                id=user.id,
                username=user.username,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_staff=user.is_staff,
                is_active=user.is_active,
                date_joined=user.date_joined,
                last_login=user.last_login,
            )
            custom_user.save()

            # Migrate user groups
            for group in user.groups.all():
                custom_user.groups.add(group)

            # Migrate user permissions
            for perm in user.user_permissions.all():
                custom_user.user_permissions.add(perm)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),  # Replace with the latest migration of the auth app
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
