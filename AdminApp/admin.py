from django.contrib import admin
from logomaker.models import users

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display=('fullname','email')


admin.site.register(users,AdminUser)
