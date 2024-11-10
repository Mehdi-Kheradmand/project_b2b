from django.contrib import admin
from .models import User


# Define an inline for RelativeProfile
# class RelativeProfileInline(admin.StackedInline):
#     model = RelativeProfile
#     verbose_name_plural = 'Relative Info'
#     extra = 0


# Customize the AccountAdmin
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)
    list_display = ('username', 'credit_balance')
    search_fields = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Accounting info', {'fields': ('credit_balance',)}),
        ('Personal info', {'fields': ('first_name', 'email')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return []
    #     inlines = []
    #     if obj.role == 'DR':
    #         inlines.append(DoctorProfileInline(self.model, self.admin_site))
    #     elif obj.role == 'EM':
    #         inlines.append(EmployeeProfileInline(self.model, self.admin_site))
    #     return inlines

    # def has_add_permission(self, request):
    #     """Disable add permission"""
    #     return False


# Register the Account model with the customized admin
admin.site.register(User, UserAdmin)
