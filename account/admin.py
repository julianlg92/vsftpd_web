from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import AccountModel, AccountGroupModel


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('label', 'username', 'last_login', 'date_joined',)
    search_fields = ('username', 'label',)
    readonly_fields = ('last_login', 'date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(AccountModel, AccountAdmin)
admin.site.register(AccountGroupModel)
