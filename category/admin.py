from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'cat_image')

    # readonly_fields = ('cat_image',)

    def get_img(self, obj):
        if obj.cat_image:
            return mark_safe(f'<img src="{obj.cat_image.url}" width="80px">')
        else:
            return 'Нет изображения'

    get_img.short_description = 'image'


admin.site.register(Category, CategoryAdmin)
