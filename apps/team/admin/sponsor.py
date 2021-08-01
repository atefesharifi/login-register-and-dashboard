from django.contrib import admin

from ..models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id', 's_name', 'logo', 'kind']
    search_fields = ['s_name']
    list_display_links = ['s_name']
