from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-is_staff', 'email')
    readonly_fields = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)