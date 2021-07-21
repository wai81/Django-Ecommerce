from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    # настройка полей для отображения в админ панели
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    # настройка полей для перехода по ссылке в админ панели
    list_display_links = ('email', 'first_name', 'last_name')
    # колонки только для чтения
    readonly_fields = ('last_login', 'date_joined')
    # сортирвка по колонке
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
