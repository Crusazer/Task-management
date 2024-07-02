from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'role')
    search_fields = ('username', 'email', 'name', 'role')
    list_filter = ('role',)
    fields = ('username', 'email', "get_phone", 'name', 'role', "photo")
    readonly_fields = ('username', 'role', "photo", "get_phone")

    def get_phone(self, phone):
        return phone.as_e164

    get_phone.short_description = 'Phone'
