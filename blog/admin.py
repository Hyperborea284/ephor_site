from django.contrib import admin
from .models import UserAccessLog

class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'latitude', 'longitude', 'user_agent')
    search_fields = ('ip_address', 'user_agent')

admin.site.register(UserAccessLog, UserAccessLogAdmin)