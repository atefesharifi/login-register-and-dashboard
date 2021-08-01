from django.contrib import admin

from ..models import TeamUser


@admin.register(TeamUser)
class TeamUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'first_name', 'last_name']
    search_fields = ['team']
    list_display_links = ['first_name']
