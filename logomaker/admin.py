from django.contrib import admin
from .models import category,product,logoinfo,client

# Register your models here.
admin.site.register(category)
admin.site.register(product)
admin.site.register(logoinfo)
admin.site.register(client)