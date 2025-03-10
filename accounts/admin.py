from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.
@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    model = get_user_model()

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email']