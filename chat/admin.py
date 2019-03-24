from django.contrib import admin

from .models import *

admin.site.register(AgentInfo)
admin.site.register(UserInfo)
admin.site.register(Company)
admin.site.register(InsuranceType)
admin.site.register(Addons)
admin.site.register(Vehicle)
admin.site.register(Insurance)
admin.site.register(Schedule)

# Register your models here.
