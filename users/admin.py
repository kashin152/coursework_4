from django.contrib import admin
from users.models import CustomsUser


@admin.register(CustomsUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")