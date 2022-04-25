from django.contrib import admin
from .models import User, ReportUser

# Register your models here.
admin.site.register(User)
admin.site.register(ReportUser)