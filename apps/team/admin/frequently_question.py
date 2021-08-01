from django.contrib import admin

from ..models import FrequentlyQuestions


@admin.register(FrequentlyQuestions)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer']
    search_fields = ['question']
    list_display_links = ['id']