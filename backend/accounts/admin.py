from django.contrib import admin
from .models import User, UserSession

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "auth_provider", "is_active", "is_staff", "created_at")
    search_fields = ("email",)
    list_filter = ("auth_provider", "is_active", "is_staff",)

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "expires_at", "revoked")
    list_filter = ("revoked",)
