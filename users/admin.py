from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from users.models import Employee

User = get_user_model()


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'role')
    search_fields = ('username', 'email', 'name', 'role')
    list_filter = ('role',)
    fields = ('id', 'username', 'email', "phone", 'name', 'display_photo', 'photo', 'role', 'can_see_all_tasks')
    readonly_fields = ('id', 'role', 'display_photo')

    def display_photo(self, obj):
        profile_photo = obj.photo
        if profile_photo:
            return mark_safe(f'<img src="{profile_photo.url}" width="50" height="50" />')
        return "No profile_photo"

    display_photo.short_description = "Display profile photo"
