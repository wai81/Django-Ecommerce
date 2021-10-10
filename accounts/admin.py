from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account, UserProfile


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


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))

    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
