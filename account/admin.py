from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin
from account.models import AccountModel, AccountGroupModel


# Register your models here.
@register(AccountModel)
class AccountAdmin(ModelAdmin):
    icon_name = 'person'
    list_display = ('label', 'username', 'last_login', 'date_joined',)
    search_fields = ('username', 'label',)
    readonly_fields = ('last_login', 'date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(AccountGroupModel)
