from django.contrib import admin

from apps.home.models.rules import Rules
from apps.home.models.sponsor import Sponsor

admin.site.register(Sponsor)
admin.site.register(Rules)

