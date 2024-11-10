from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'charge_balance')


admin.site.register(Phone, PhoneAdmin)
