from django.contrib import admin

from ..models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'en_name', 'fa_name', 'phone', 'verify_phone']
    search_fields = ['en_name']
    list_display_links = ['en_name']
