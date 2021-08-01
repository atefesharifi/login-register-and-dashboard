from django.contrib import admin
from apps.team.models.team import Team
from apps.team.models.team_user import TeamUser
from apps.accounts.models.user import User
from apps.team.models.rules import Rules


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ['username', 'team']


admin.site.register(Team)
admin.site.register(TeamUser)
admin.site.register(Rules)
