from django.contrib import admin

from apps.accounts.models.team import Team
from apps.accounts.models.team_user import TeamUser
from apps.accounts.models.user import User


class TeamUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'first_name', 'last_name']


admin.site.register(Team)
admin.site.register(User)
admin.site.register(TeamUser, TeamUserAdmin)
