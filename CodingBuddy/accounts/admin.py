from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group


# Unregister the default User admin
admin.site.unregister(User)

# Register the default User admin with custom actions
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'get_groups']
    actions = ['approve_developers']

    def get_groups(self, instance):
        return ", ".join([group.name for group in instance.groups.all()])
    get_groups.short_description = 'Groups'

    def approve_developers(self, request, queryset):
        developer_group = Group.objects.get(name='Developer')
        for user in queryset:
            if developer_group in user.groups.all():
                user.is_active = True
                user.save()
    approve_developers.short_description = "Approve selected developers"

admin.site.register(User, CustomUserAdmin)


